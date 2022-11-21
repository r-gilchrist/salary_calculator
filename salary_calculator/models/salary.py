from typing import List
from marshmallow import Schema, fields, post_load
from datetime import datetime

from salary_calculator.helpers.frequency_helpers import frequency_dependent, PaymentFrequency
from salary_calculator.helpers.tax_helpers import TaxApplied
from salary_calculator.models.date import Date, DateSchema
from salary_calculator.models.pension import Pension, PensionSchema
from salary_calculator.models.salary_sacrifice import SalarySacrifice, SalarySacrificeSchema
from salary_calculator.models.student_loan import StudentLoan, StudentLoanSchema
from salary_calculator.models.national_insurance import NationalInsurance, NationalInsuranceSchema
from salary_calculator.models.income_tax import IncomeTax, IncomeTaxSchema
from salary_calculator.models.taxable_benefit import TaxableBenefits, TaxableBenefitsSchema
from salary_calculator.models.requests.benefits_summary import BenefitsSummary
from salary_calculator.models.requests.salary_summary import SalarySummary
from salary_calculator.models.requests.tax_summary import TaxSummary


class Salary:

    def __init__(self,
                 reference_salary: float,
                 taxable_benefits: List[TaxableBenefits] = None,
                 pension: Pension = None,
                 salary_sacrifices: List[SalarySacrifice] = None,
                 income_tax: IncomeTax = None,
                 national_insurance: NationalInsurance = None,
                 student_loan: StudentLoan = None,
                 date: Date = None):

        self.reference_salary = reference_salary
        self.taxable_benefits = taxable_benefits or []
        self.pension = pension or Pension()
        self.salary_sacrifices = salary_sacrifices or []
        self.date = date or Date(year=datetime.now().year, month=datetime.now().month)
        if student_loan is not None:
            self.student_loan = StudentLoan(date=self.date.as_datetime(), plan=student_loan.plan)
        else:
            self.student_loan = StudentLoan()
        self.income_tax = income_tax or IncomeTax(self.date.as_datetime())
        self.national_insurance = national_insurance or NationalInsurance(self.date.as_datetime())
        self.gross_salary = self.get_gross_salary()

    @frequency_dependent
    def get_reference_salary(self, frequency: PaymentFrequency = PaymentFrequency.ANNUAL):
        return self.reference_salary

    @frequency_dependent
    def get_gross_salary(self, frequency: PaymentFrequency = PaymentFrequency.ANNUAL):
        return self.reference_salary - self.get_pension_my_contribution() - self.get_salary_sacrifices()

    @frequency_dependent
    def get_taxable_benefits(self, frequency: PaymentFrequency = PaymentFrequency.ANNUAL):
        return sum([benefit.get_amount() for benefit in self.taxable_benefits])

    @frequency_dependent
    def get_pension(self, frequency: PaymentFrequency = PaymentFrequency.ANNUAL):
        return self.pension.get_amount(self.reference_salary)

    @frequency_dependent
    def get_pension_my_contribution(self, frequency: PaymentFrequency = PaymentFrequency.ANNUAL):
        return self.pension.get_amount_my_contribution(self.reference_salary)

    @frequency_dependent
    def get_salary_sacrifices(self, frequency: PaymentFrequency = PaymentFrequency.ANNUAL, sacrifice_type: str = "all"):
        if sacrifice_type == "all":
            return sum([sacrifice.get_amount() for sacrifice in self.salary_sacrifices])
        sacrifices = [sacrifice for sacrifice in self.salary_sacrifices if sacrifice.sacrifice_type == sacrifice_type]
        return sum([sacrifice.get_amount() for sacrifice in sacrifices])

    @frequency_dependent
    def get_income_tax(self, frequency: PaymentFrequency = PaymentFrequency.ANNUAL):
        taxed_sacrifices = [sacrifice for sacrifice in self.salary_sacrifices if
                            sacrifice.sacrifice_type == TaxApplied.NI_ONLY]

        return self.income_tax.get_amount(self.gross_salary +
                                          self.get_taxable_benefits() +
                                          sum([sacrifice.get_amount() for sacrifice in taxed_sacrifices]))

    @frequency_dependent
    def get_national_insurance(self, frequency: PaymentFrequency = PaymentFrequency.ANNUAL):
        return self.national_insurance.get_amount(self.gross_salary)

    @frequency_dependent
    def get_student_loan(self, frequency: PaymentFrequency = PaymentFrequency.ANNUAL):
        return self.student_loan.get_amount(self.gross_salary)

    @frequency_dependent
    def get_take_home(self, frequency: PaymentFrequency = PaymentFrequency.ANNUAL):
        take_home = (self.reference_salary -
                     self.get_pension_my_contribution() -
                     self.get_salary_sacrifices() -
                     self.get_income_tax() -
                     self.get_national_insurance() -
                     self.get_student_loan())
        return take_home

    def get_salary_summary(self, frequency: PaymentFrequency = PaymentFrequency.ANNUAL):

        salary_summary = SalarySummary(
            reference_salary=self.get_reference_salary(frequency=frequency),
            take_home=self.get_take_home(frequency=frequency))

        return salary_summary

    def get_benefits_summary(self, frequency: PaymentFrequency = PaymentFrequency.ANNUAL):

        benefits_summary = BenefitsSummary(
            salary_sacrifice=self.get_salary_sacrifices(frequency=frequency),
            taxable_benefit=self.get_taxable_benefits(frequency=frequency),
            pension=self.get_pension(frequency=frequency))

        return benefits_summary

    def get_tax_summary(self, frequency: PaymentFrequency = PaymentFrequency.ANNUAL):

        tax_summary = TaxSummary(
            income_tax=self.get_income_tax(frequency=frequency),
            national_insurance=self.get_national_insurance(frequency=frequency),
            student_loan=self.get_student_loan(frequency=frequency))

        return tax_summary


class SalarySchema(Schema):

    date = fields.Nested(DateSchema, required=False)
    reference_salary = fields.Integer(required=True)
    taxable_benefits = fields.List(fields.Nested(TaxableBenefitsSchema), required=False)
    pension = fields.Nested(PensionSchema, required=False)
    salary_sacrifices = fields.List(fields.Nested(SalarySacrificeSchema), required=False)
    income_tax = fields.Nested(IncomeTaxSchema, required=False)
    student_loan = fields.Nested(StudentLoanSchema, required=False)
    national_insurance = fields.Nested(NationalInsuranceSchema, required=False)

    @post_load
    def make_data(self, data, **_kwargs) -> Salary:
        return Salary(**data)

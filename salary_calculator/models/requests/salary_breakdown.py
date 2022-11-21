from marshmallow import Schema, fields, post_load
from marshmallow_enum import EnumField
from salary_calculator.helpers.frequency_helpers import PaymentFrequency
from salary_calculator.models.requests.benefits_summary import BenefitsSummary, BenefitsSummarySchema
from salary_calculator.models.requests.salary_summary import SalarySummary, SalarySummarySchema
from salary_calculator.models.requests.tax_summary import TaxSummary, TaxSummarySchema


class SalaryBreakdown:

    def __init__(self,
                 date_calculated_for: str,
                 frequency: PaymentFrequency,
                 salary_summary: SalarySummary,
                 benefits_summary: BenefitsSummary,
                 tax_summary: TaxSummary):

        self.date_calculated_for = date_calculated_for
        self.frequency = frequency
        self.salary_summary = salary_summary
        self.benefits_summary = benefits_summary
        self.tax_summary = tax_summary


class SalaryBreakdownSchema(Schema):

    date_calculated_for = fields.String(required=True)
    frequency = EnumField(PaymentFrequency, required=True)
    salary_summary = fields.Nested(SalarySummarySchema, required=True)
    benefits_summary = fields.Nested(BenefitsSummarySchema, required=True)
    tax_summary = fields.Nested(TaxSummarySchema, required=True)

    @post_load
    def make_data(self, data, **_kwargs) -> SalaryBreakdown:
        return SalaryBreakdown(**data)

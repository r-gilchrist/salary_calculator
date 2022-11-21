from flask_restful import Resource, Api
from flask import Blueprint, request

from datetime import datetime
from salary_calculator.helpers.frequency_helpers import PaymentFrequency
from salary_calculator.models.salary import SalarySchema

from salary_calculator.models.requests.benefits_summary import BenefitsSummarySchema
from salary_calculator.models.requests.salary_summary import SalarySummarySchema
from salary_calculator.models.requests.tax_summary import TaxSummarySchema
from salary_calculator.models.requests.salary_breakdown import SalaryBreakdownSchema, SalaryBreakdown


class SalaryBreakdownRequest(Resource):

    @staticmethod
    def post(frequency: str):

        data = request.json
        include_policy_changes = data.pop("include_policy_changes", False)
        salary = SalarySchema().load(data)

        breakdown = SalaryBreakdown(
            date_calculated_for=datetime.strftime(salary.date.as_datetime(), "%Y-%m"),
            frequency=PaymentFrequency(frequency),
            salary_summary=SalarySummarySchema().dump(
                salary.get_salary_summary(frequency=PaymentFrequency(frequency))),
            benefits_summary=BenefitsSummarySchema().dump(
                salary.get_benefits_summary(frequency=PaymentFrequency(frequency))),
            tax_summary=TaxSummarySchema().dump(
                salary.get_tax_summary(frequency=PaymentFrequency(frequency)))
        )

        response = SalaryBreakdownSchema().dump(breakdown)

        if include_policy_changes:
            policy_changes = {
                "student_loan": salary.student_loan.get_change_from_present_day(),
                "national_insurance": salary.national_insurance.get_change_from_present_day(),
                "income_tax": salary.income_tax.get_change_from_present_day()
            }
            response["policy_changes"] = policy_changes

        return response, 201


bp = Blueprint("salary_breakdown", __name__)
api = Api(bp)
api.add_resource(SalaryBreakdownRequest, "/salary_breakdown/<string:frequency>")

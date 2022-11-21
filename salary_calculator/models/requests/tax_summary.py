from marshmallow import Schema, fields, post_load


class TaxSummary:

    def __init__(self,
                 income_tax: float,
                 national_insurance: float,
                 student_loan: float):

        self.income_tax = self._to_currency(income_tax)
        self.national_insurance = self._to_currency(national_insurance)
        self.student_loan = self._to_currency(student_loan)

    @staticmethod
    def _to_currency(value: float) -> str:
        return f"£{value:,.2f}"


class TaxSummarySchema(Schema):

    income_tax: float = fields.String(required=True)
    national_insurance: float = fields.String(required=True)
    student_loan: float = fields.String(required=True)

    @post_load
    def make_data(self, data, **_kwargs) -> TaxSummary:
        return TaxSummary(**data)

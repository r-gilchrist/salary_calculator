from marshmallow import Schema, fields, post_load


class BenefitsSummary:

    def __init__(self,
                 salary_sacrifice: float,
                 taxable_benefit: float,
                 pension: float):

        self.salary_sacrifice = self._to_currency(salary_sacrifice)
        self.taxable_benefit = self._to_currency(taxable_benefit)
        self.pension = self._to_currency(pension)

    @staticmethod
    def _to_currency(value: float) -> str:
        return f"£{value:,.2f}"


class BenefitsSummarySchema(Schema):

    salary_sacrifice = fields.String(required=True)
    pension: float = fields.String(required=True)
    taxable_benefit = fields.String(required=True)

    @post_load
    def make_data(self, data, **_kwargs) -> BenefitsSummary:
        return BenefitsSummary(**data)

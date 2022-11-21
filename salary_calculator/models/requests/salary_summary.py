from marshmallow import Schema, fields, post_load


class SalarySummary:

    def __init__(self,
                 reference_salary: float,
                 take_home: float):

        self.reference_salary = self._to_currency(reference_salary)
        self.take_home = self._to_currency(take_home)

    @staticmethod
    def _to_currency(value: float) -> str:
        return f"£{value:,.2f}"


class SalarySummarySchema(Schema):

    reference_salary = fields.String(required=True)
    take_home: float = fields.String(required=True)

    @post_load
    def make_data(self, data, **_kwargs) -> SalarySummary:
        return SalarySummary(**data)

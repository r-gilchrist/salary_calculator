from marshmallow import Schema, fields, post_load
from salary_calculator.helpers.frequency_helpers import PaymentFrequency


class TaxableBenefits:

    def __init__(self, value: int, frequency: PaymentFrequency = PaymentFrequency.ANNUAL):
        self.value = value
        self.frequency = frequency

    def get_amount(self):
        if self.frequency == PaymentFrequency.MONTHLY:
            return self.value * 12
        if self.frequency == PaymentFrequency.ANNUAL:
            return self.value


class TaxableBenefitsSchema(Schema):

    value = fields.Integer(required=True)
    frequency = fields.String(required=False)

    @post_load
    def make_data(self, data, **_kwargs) -> TaxableBenefits:
        return TaxableBenefits(**data)

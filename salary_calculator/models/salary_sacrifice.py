from marshmallow import Schema, fields, post_load
from marshmallow_enum import EnumField

from salary_calculator.helpers.frequency_helpers import PaymentFrequency
from salary_calculator.helpers.tax_helpers import TaxApplied


class SalarySacrifice:

    def __init__(self,
                 value: int,
                 frequency: PaymentFrequency = PaymentFrequency.ANNUAL,
                 sacrifice_type: TaxApplied = TaxApplied.TAX_EXEMPT):
        self.value = value
        self.frequency = frequency
        self.sacrifice_type = sacrifice_type

    def get_amount(self):
        if self.frequency == PaymentFrequency.MONTHLY:
            return self.value * 12
        if self.frequency == PaymentFrequency.ANNUAL:
            return self.value


class SalarySacrificeSchema(Schema):

    value = fields.Integer(required=True)
    frequency = EnumField(PaymentFrequency, required=False)
    sacrifice_type = EnumField(TaxApplied, required=False)

    @post_load
    def make_data(self, data, **_kwargs) -> SalarySacrifice:
        return SalarySacrifice(**data)

from unittest import TestCase
from marshmallow import ValidationError
from datetime import datetime
from salary_calculator.models.income_tax import IncomeTax, IncomeTaxSchema


class IncomeTaxSchemaTests(TestCase):

    def test_roundtrip_conversion(self):

        income_tax = IncomeTax(date=datetime(year=2020, month=3, day=1))

        income_tax_dict = IncomeTaxSchema().dump(income_tax)
        roundtrip = IncomeTaxSchema().load(income_tax_dict)

        self.assertEqual(income_tax.date, roundtrip.date)

    def test_validation_error_is_raised_with_missing_required_input(self):

        data_dict = {}

        with self.assertRaises(ValidationError):
            IncomeTaxSchema().load(data_dict)

    def test_validation_error_is_raised_with_unexpected_key(self):

        data_dict = {
            "bad_key": "some_value"
        }

        with self.assertRaises(ValidationError):
            IncomeTaxSchema().load(data_dict)

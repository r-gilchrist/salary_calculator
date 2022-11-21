from unittest import TestCase
from marshmallow import ValidationError
from salary_calculator.models.pension import Pension, PensionSchema


class PensionSchemaTests(TestCase):

    def test_roundtrip_conversion_with_all_parameters(self):

        pension = Pension(my_contribution=2, employer_contribution=6)

        pension_dict = PensionSchema().dump(pension)
        roundtrip = PensionSchema().load(pension_dict)

        self.assertEqual(pension.my_contribution, roundtrip.my_contribution)
        self.assertEqual(pension.employer_contribution, roundtrip.employer_contribution)

    def test_pensions_can_be_defined_without_specifying_values(self):

        data_dict = {}
        pension = PensionSchema().load(data_dict)
        self.assertEqual(0, pension.my_contribution)
        self.assertEqual(0, pension.employer_contribution)

        data_dict = {"my_contribution": 10}
        pension = PensionSchema().load(data_dict)
        self.assertEqual(10, pension.my_contribution)
        self.assertEqual(0, pension.employer_contribution)

        data_dict = {"employer_contribution": 6.5}
        pension = PensionSchema().load(data_dict)
        self.assertEqual(0, pension.my_contribution)
        self.assertEqual(6.5, pension.employer_contribution)

    def test_validation_error_is_raised_with_unexpected_key(self):

        data_dict = {
            "bad_key": "some_value"
        }

        with self.assertRaises(ValidationError):
            PensionSchema().load(data_dict)

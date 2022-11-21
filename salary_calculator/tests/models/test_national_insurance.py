from unittest import TestCase
from marshmallow import ValidationError
from datetime import datetime
from salary_calculator.models.national_insurance import NationalInsurance, NationalInsuranceSchema


class NationalInsuranceSchemaTests(TestCase):

    def test_roundtrip_conversion_with_all_parameters(self):

        national_insurance = NationalInsurance(
            date=datetime(year=2020, month=3, day=1),
            basic_rate=0.10,
            basic_threshold=10000,
            higher_rate=0.3,
            higher_threshold=100000)

        national_insurance_dict = NationalInsuranceSchema().dump(national_insurance)
        roundtrip = NationalInsuranceSchema().load(national_insurance_dict)

        self.assertEqual(national_insurance.date, roundtrip.date)
        self.assertEqual(national_insurance.basic_rate, roundtrip.basic_rate)
        self.assertEqual(national_insurance.basic_threshold, roundtrip.basic_threshold)
        self.assertEqual(national_insurance.higher_rate, roundtrip.higher_rate)
        self.assertEqual(national_insurance.higher_threshold, roundtrip.higher_threshold)

    def test_validation_error_is_raised_with_unexpected_key(self):

        data_dict = {
            "bad_key": "some_value"
        }

        with self.assertRaises(ValidationError):
            NationalInsuranceSchema().load(data_dict)

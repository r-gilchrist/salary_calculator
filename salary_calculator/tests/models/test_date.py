from unittest import TestCase
from marshmallow import ValidationError
from salary_calculator.models.date import Date, DateSchema


class DateTests(TestCase):

    def test_roundtrip_conversion(self):

        date = Date(year=2022, month=1)

        date_dict = DateSchema().dump(date)
        roundtrip = DateSchema().load(date_dict)

        self.assertEqual(date.year, roundtrip.year)
        self.assertEqual(date.month, roundtrip.month)

    def test_validation_error_is_raised_with_missing_required_input(self):

        data_dict = {
            "month": 12
        }

        with self.assertRaises(ValidationError):
            DateSchema().load(data_dict)

    def test_validation_error_is_raised_with_unexpected_key(self):

        data_dict = {
            "year": 2022,
            "bad_key": "some_value"
        }

        with self.assertRaises(ValidationError):
            DateSchema().load(data_dict)

    def test_validation_error_is_raised_with_invalid_month(self):

        bad_months = [-1, 0, 13, 99]

        for bad_month in bad_months:
            data_dict = {
                "year": 2022,
                "month": bad_month
            }

            with self.assertRaises(ValidationError):
                DateSchema().load(data_dict)

    def test_validation_error_is_raised_with_invalid_year(self):

        bad_years = [2017, 2018, 2019]

        for bad_year in bad_years:
            data_dict = {
                "year": 2022,
                "month": bad_year
            }

            with self.assertRaises(ValidationError):
                DateSchema().load(data_dict)

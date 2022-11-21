from datetime import datetime
from typing import Optional
from marshmallow import Schema, fields, post_load
from salary_calculator.data import get_rate, get_threshold


class NationalInsurance:

    def __init__(self,
                 date: datetime.date = datetime.now(),
                 basic_rate: Optional[float] = None,
                 basic_threshold: Optional[int] = None,
                 higher_rate: Optional[float] = None,
                 higher_threshold: Optional[int] = None):
        self.date = date
        self.basic_rate = basic_rate or self.get_basic_rate_from_date()
        self.basic_threshold = basic_threshold or self.get_basic_threshold_from_date()
        self.higher_rate = higher_rate or self.get_higher_rate_from_date()
        self.higher_threshold = higher_threshold or self.get_higher_threshold_from_date()

    def get_basic_rate_from_date(self):
        return get_rate("national_insurance", "basic", self.date)

    def get_basic_threshold_from_date(self):
        return get_threshold("national_insurance", "basic", self.date)

    def get_higher_rate_from_date(self):
        return get_rate("national_insurance", "higher", self.date)

    def get_higher_threshold_from_date(self):
        return get_threshold("national_insurance", "higher", self.date)

    def _get_basic_contribution(self, gross_salary: int):
        if gross_salary < self.basic_threshold:
            return 0
        _valid_salary = min(gross_salary - self.basic_threshold, self.higher_threshold - self.basic_threshold)
        return _valid_salary * self.basic_rate

    def _get_higher_contribution(self, gross_salary: int):
        if gross_salary <= self.higher_threshold:
            return 0
        _valid_salary = gross_salary - self.higher_threshold
        return self.higher_rate * _valid_salary

    def get_amount(self, gross_salary: int):
        return self._get_basic_contribution(gross_salary) + self._get_higher_contribution(gross_salary)

    def get_change_from_present_day(self):
        present_day = NationalInsurance()

        present_summary = {"basic_rate": present_day.basic_rate,
                           "basic_threshold": present_day.basic_threshold,
                           "higher_rate": present_day.higher_rate,
                           "higher_threshold": present_day.higher_threshold}

        self_summary = {"basic_rate": self.basic_rate,
                        "basic_threshold": self.basic_threshold,
                        "higher_rate": self.higher_rate,
                        "higher_threshold": self.higher_threshold}

        differences = {}
        for key in self_summary:
            if present_summary[key] != self_summary[key]:
                differences[key] = {
                    "present day": present_summary[key],
                    "this calculation": self_summary[key]
                }

        return differences


class NationalInsuranceSchema(Schema):

    date = fields.DateTime(required=False)
    basic_rate = fields.Float(required=False)
    basic_threshold = fields.Integer(required=False)
    higher_rate = fields.Float(required=False)
    higher_threshold = fields.Integer(required=False)

    @post_load
    def make_data(self, data, **_kwargs) -> NationalInsurance:
        return NationalInsurance(**data)

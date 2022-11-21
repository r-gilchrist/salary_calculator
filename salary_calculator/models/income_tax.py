from datetime import datetime
from marshmallow import Schema, fields, post_load
from salary_calculator.data import get_rate, get_threshold


class IncomeTax:

    def __init__(self, date: datetime.date = datetime.now()):
        self.date = date

    def basic_rate(self):
        return get_rate("income_tax", "basic", self.date)

    def basic_threshold(self):
        return get_threshold("income_tax", "basic", self.date)

    def higher_rate(self):
        return get_rate("income_tax", "higher", self.date)

    def higher_threshold(self):
        return get_threshold("income_tax", "higher", self.date)

    def additional_rate(self):
        return get_rate("income_tax", "additional", self.date)

    def additional_threshold(self):
        return get_threshold("income_tax", "additional", self.date)

    def _get_basic_contribution(self, gross_salary: int):
        if gross_salary < self.basic_threshold():
            return 0
        _valid_salary = min(gross_salary - self.basic_threshold(), self.higher_threshold() - self.basic_threshold())
        return _valid_salary * self.basic_rate()

    def _get_higher_contribution(self, gross_salary: int):
        if gross_salary <= self.higher_threshold():
            return 0
        _valid_salary = min(gross_salary - self.higher_threshold(),
                            self.additional_threshold() - self.higher_threshold())
        return self.higher_rate() * _valid_salary

    def _get_additional_contribution(self, gross_salary: int):
        if gross_salary < self.additional_threshold():
            return 0
        _valid_salary = gross_salary - self.additional_threshold()
        return self.additional_rate() * _valid_salary

    def get_amount(self, gross_salary: int):
        return self._get_basic_contribution(gross_salary) +\
               self._get_higher_contribution(gross_salary) +\
               self._get_additional_contribution(gross_salary)

    def get_change_from_present_day(self):
        present_day = IncomeTax()

        present_summary = {"basic_rate": present_day.basic_rate(),
                           "basic_threshold": present_day.basic_threshold(),
                           "higher_rate": present_day.higher_rate(),
                           "higher_threshold": present_day.higher_threshold(),
                           "additional_rate": present_day.additional_rate(),
                           "additional_threshold": present_day.additional_threshold()}

        self_summary = {"basic_rate": self.basic_rate(),
                        "basic_threshold": self.basic_threshold(),
                        "higher_rate": self.higher_rate(),
                        "higher_threshold": self.higher_threshold(),
                        "additional_rate": self.additional_rate(),
                        "additional_threshold": self.additional_threshold()}

        differences = {}
        for key in self_summary:
            if present_summary[key] != self_summary[key]:
                differences[key] = {
                    "present day": present_summary[key],
                    "this calculation": self_summary[key]
                }

        return differences


class IncomeTaxSchema(Schema):

    date = fields.DateTime(required=True)

    @post_load
    def make_data(self, data, **_kwargs) -> IncomeTax:
        return IncomeTax(**data)

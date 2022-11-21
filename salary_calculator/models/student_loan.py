from typing import Optional
from marshmallow import Schema, fields, post_load
from datetime import datetime
from salary_calculator.data import get_threshold, get_rate


class StudentLoan:

    def __init__(self,
                 date: datetime.date = datetime.now(),
                 plan: str = "none",
                 rate: Optional[float] = None,
                 threshold: Optional[int] = None):
        self.date = date
        self.plan = plan
        self.rate = rate or self.get_rate_from_date()
        self.threshold = threshold or self.get_threshold_from_date()

    def get_threshold_from_date(self):
        if self.plan == "none":
            return 0
        return get_threshold("student_loan", self.plan, self.date)

    def get_rate_from_date(self):
        if self.plan == "none":
            return 0
        return get_rate("student_loan", self.plan, self.date)

    def get_amount(self, gross_salary: int):
        if gross_salary <= self.threshold:
            return 0
        _valid_salary = gross_salary - self.threshold
        return int(self.rate * _valid_salary / 12) * 12

    def get_change_from_present_day(self):
        present_day = StudentLoan(plan=self.plan)

        present_summary = {"rate": present_day.rate,
                           "threshold": present_day.threshold}

        self_summary = {"rate": self.rate,
                        "threshold": self.threshold}

        differences = {}
        for key in self_summary:
            if present_summary[key] != self_summary[key]:
                differences[key] = {
                    "present day": present_summary[key],
                    "this calculation": self_summary[key]
                }

        return differences


class StudentLoanSchema(Schema):

    plan = fields.String(required=False)
    date = fields.DateTime(required=False)
    rate = fields.Float(required=False)
    threshold = fields.Integer(required=False)

    @post_load
    def make_data(self, data, **_kwargs) -> StudentLoan:
        return StudentLoan(**data)

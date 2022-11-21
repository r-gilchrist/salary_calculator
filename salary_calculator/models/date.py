from marshmallow import Schema, fields, post_load, validates, ValidationError
from datetime import datetime


class Date:

    def __init__(self, year: int, month: int = 4):
        self.year = year
        self.month = month

    def as_datetime(self):
        return datetime(year=self.year, month=self.month, day=1)


class DateSchema(Schema):

    year = fields.Int(required=True)
    month = fields.Int(required=False)

    @validates("year")
    def validate_year(self, year, **kwargs):
        if year < 2020:
            raise ValidationError("Year must be at least 2020")

    @validates("month")
    def validate_month(self, month, **kwargs):
        if month < 1 or month > 12:
            raise ValidationError("Invalid month. Must be between 1 and 12")

    @post_load
    def make_data(self, data, **_kwargs) -> Date:
        return Date(**data)

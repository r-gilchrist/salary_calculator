from marshmallow import Schema, fields, post_load


class Pension:

    def __init__(self, my_contribution: float = 0, employer_contribution: float = 0):
        self.my_contribution = my_contribution
        self.employer_contribution = employer_contribution

    def get_amount(self, reference_salary: float):
        return self.get_amount_my_contribution(reference_salary) +\
               self.get_amount_employer_contribution(reference_salary)

    def get_amount_my_contribution(self, reference_salary: float):
        return reference_salary * self.my_contribution / 100

    def get_amount_employer_contribution(self, reference_salary: float):
        return reference_salary * self.employer_contribution / 100


class PensionSchema(Schema):

    my_contribution = fields.Float(required=False)
    employer_contribution = fields.Float(required=False)

    @post_load
    def make_data(self, data, **_kwargs) -> Pension:
        return Pension(**data)

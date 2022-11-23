# salary_calculator

Salary calculator module written in Python. Currently in prototyping stage, so don't expect everything to work!

THis repository consists of a few things:

1. Code to calculate salary based on things such as income tax, national insurance etc.
2. A Flask application as an interface to using the code

Instructions TBC once I've finalised exactly how this will be set up! But as an example, once your server is loaded up you can send a request such as:

```
{
    "reference_salary": 50000,
    "pension": {
        "my_contribution": 5,
        "employer_contribution": 5
    },
    "student_loan": {
        "plan": "plan_1"
    }
}
```

and receive the following response:

```
{
    "benefits_summary": {
        "taxable_benefit": "£0.00",
        "pension": "£416.67",
        "salary_sacrifice": "£0.00"
    },
    "date_calculated_for": "2022-11",
    "frequency": "MONTHLY",
    "tax_summary": {
        "income_tax": "£582.17",
        "national_insurance": "£349.30",
        "student_loan": "£204.00"
    },
    "salary_summary": {
        "reference_salary": "£4,166.67",
        "take_home": "£2,822.87"
    }
}
```



### Roadmap to v0.2.0

- Full test coverage
- Server to be protected against edge cases
- Swagger documentation for the API

### Roadmap to v0.3.0

- Support for bonuses
- Next 12 months summary + other endpoints
- docker-compose deployment

### Future - a frontend

Eventually there will be a html-based frontend to the app. The idea is to allow for real-time updates of your calculations as you type numbers in, and full flexibility of the assumptions (something existing tools don't do).

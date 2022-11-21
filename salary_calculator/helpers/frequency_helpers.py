from functools import wraps
from enum import Enum


class PaymentFrequency(Enum):

    ANNUAL = "annual"
    MONTHLY = "monthly"
    WEEKLY = "weekly"
    DAILY = "daily"


def frequency_dependent(func):

    @wraps(func)
    def inner(*args, **kwargs):
        value = func(*args, **kwargs)
        frequency = kwargs.get("frequency", PaymentFrequency.ANNUAL)

        if frequency == PaymentFrequency.MONTHLY:
            return value / 12
        if frequency == PaymentFrequency.WEEKLY:
            return value / 52
        if frequency == PaymentFrequency.DAILY:
            return value / 260
        return value

    return inner

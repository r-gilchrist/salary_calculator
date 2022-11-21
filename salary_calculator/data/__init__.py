from datetime import datetime
import json
from pathlib import Path

JSON_FILE = f"{Path(__file__).parent}/rates_and_thresholds.json"


def datetime_from_string(date: str) -> datetime.date:
    return datetime.strptime(date, "%Y-%m")


def _get_value(value_type: str, tax_type: str, category: str, date: datetime.date) -> int:

    with open(JSON_FILE, "r") as f:
        data = json.load(f)

    values = data[value_type][tax_type][category]

    for value in values:
        date_start = datetime.strptime(value["date_start"], "%Y-%m")
        date_end = datetime.strptime(value["date_end"], "%Y-%m")

        if date_start <= date < date_end:
            return value["value"]

    return _get_value(value_type, tax_type, category, datetime.now())


def get_rate(tax_type: str, category: str, date: datetime.date) -> int:
    return _get_value("rate", tax_type, category, date)


def get_threshold(tax_type: str, category: str, date: datetime.date) -> int:
    return _get_value("threshold", tax_type, category, date)

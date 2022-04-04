from datetime import date
from dateutil import rrule, relativedelta

from cohortextractor import patients


def last_day_of_month(dt):
    return dt + relativedelta.relativedelta(day=31)


def calculate_months(start_date, end_date, selected_codelist):
    months = {}
    for start_of_month in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
        start = date.strftime(start_of_month, "%Y-%m-%d")
        end = date.strftime(last_day_of_month(start_of_month), "%Y-%m-%d")
        months[f"{start}"] = patients.with_these_clinical_events(
            codelist=selected_codelist,
            between=[start, end],
            returning="number_of_episodes",
            return_expectations={
                "int": {"distribution": "normal", "mean": 2, "stddev": 0.5}
            },
        )

    return months

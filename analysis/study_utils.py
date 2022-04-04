from datetime import date
from dateutil import rrule, relativedelta

from cohortextractor import patients, codelist


def last_day_of_month(dt):
    return dt + relativedelta.relativedelta(day=31)


def calculate_months(start_date, end_date, selected_codelist):
    months = {}
    for start_of_month in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
        start = date.strftime(start_of_month, "%Y-%m-%d")
        end = date.strftime(last_day_of_month(start_of_month), "%Y-%m-%d")
        months[f"episode_{start}"] = patients.with_these_clinical_events(
            codelist=selected_codelist,
            between=[start, end],
            episode_defined_as="series of events each <= 0 days apart",
            returning="number_of_episodes",
            return_expectations={
                "int": {"distribution": "normal", "mean": 2, "stddev": 0.5}
            },
        )

    return months


def calculate_code_frequency(start_date, end_date, selected_codes):
    start_date_formatted = date.strftime(start_date, "%Y-%m-%d")
    end_date_formatted = date.strftime(end_date, "%Y-%m-%d")

    variables = {}
    for code in selected_codes:
        variables[f"snomed_{code}"] = patients.with_these_clinical_events(
                codelist([code], system="snomed"),
                between=[start_date_formatted, end_date_formatted],
                returning="number_of_matches_in_period",
                return_expectations={
                    "incidence": 0.1,
                    "int": {"distribution": "normal", "mean": 3, "stddev": 1},
                }
        )
    return variables

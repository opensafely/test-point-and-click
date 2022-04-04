from datetime import date
from dateutil import rrule

from cohortextractor import (
    StudyDefinition,
    patients,
)

from analysis.study_utils import last_day_of_month, last_day_of_week
from variables import selected_codelist, start_date, end_date, frequency


def number_of_episodes(start, end, selected_codelist):
    return {
        f"episode_{start}":
        patients.with_these_clinical_events(
            codelist=selected_codelist,
            between=[start, end],
            episode_defined_as="series of events each <= 0 days apart",
            returning="number_of_episodes",
            return_expectations={
                "int": {"distribution": "normal", "mean": 2, "stddev": 0.5}
            },
        ),
    }


def calculate_months(start_date, end_date, selected_codelist):
    months = {}
    for start_of_month in rrule.rrule(
        rrule.MONTHLY, dtstart=start_date, until=end_date
    ):
        start = date.strftime(start_of_month, "%Y-%m-%d")
        end = date.strftime(last_day_of_month(start_of_month), "%Y-%m-%d")
        months.update(number_of_episodes(start, end, selected_codelist))

    return months


def calculate_weeks(start_date, end_date, selected_codelist):
    weeks = {}
    for start_of_week in rrule.rrule(rrule.WEEKLY, dtstart=start_date, until=end_date):
        start = date.strftime(start_of_week, "%Y-%m-%d")
        end = date.strftime(last_day_of_week(start_of_week), "%Y-%m-%d")
        weeks.update(number_of_episodes(start, end, selected_codelist))

    return weeks


index_date = date.strftime(start_date, "%Y-%m-%d")
latest_date = date.strftime(last_day_of_month(end_date), "%Y-%m-%d")

calculate_frequency = calculate_months if frequency == "monthly" else calculate_weeks

study = StudyDefinition(
    default_expectations={
        "date": {"earliest": index_date, "latest": latest_date},
        "rate": "uniform",
        "incidence": 0.5,
    },
    index_date=index_date,
    population=patients.all(),
    **calculate_frequency(start_date, end_date, selected_codelist),
)

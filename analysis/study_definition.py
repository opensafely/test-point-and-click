from datetime import date, datetime
from dateutil import rrule

from cohortextractor import (
    codelist_from_csv,
    StudyDefinition,
    patients,
)

from analysis.study_utils import last_day_of_month, last_day_of_week
from variables import codelist_file, study_start_date, study_end_date, frequency


def number_of_episodes(start, end, selected_codelist):
    return {
        f"episode_{start}": patients.with_these_clinical_events(
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


start_date = datetime.strptime(study_start_date, "%Y-%m-%d").date()
end_date = datetime.strptime(study_end_date, "%Y-%m-%d").date()

calculate_frequency = calculate_months if frequency == "monthly" else calculate_weeks

selected_codelist = codelist_from_csv(
    codelist_file,
    system="snomed",
    column="code",
)

study = StudyDefinition(
    default_expectations={
        "date": {"earliest": study_start_date, "latest": study_end_date},
        "rate": "uniform",
        "incidence": 0.5,
    },
    index_date=study_start_date,
    population=patients.all(),
    **calculate_frequency(start_date, end_date, selected_codelist),
)

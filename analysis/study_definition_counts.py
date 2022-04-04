from datetime import date

from cohortextractor import (
    StudyDefinition,
    codelist,
    patients,
)

from analysis.study_utils import last_day_of_month
from variables import selected_codelist, start_date, end_date


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
            },
        )
    return variables


index_date = date.strftime(start_date, "%Y-%m-%d")
latest_date = date.strftime(last_day_of_month(end_date), "%Y-%m-%d")

study = StudyDefinition(
    default_expectations={
        "date": {"earliest": index_date, "latest": latest_date},
        "rate": "uniform",
        "incidence": 0.5,
    },
    index_date=index_date,
    population=patients.all(),
    **calculate_code_frequency(start_date, end_date, selected_codelist),
)

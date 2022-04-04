from datetime import date

from cohortextractor import (
    StudyDefinition,
    patients,
)

from analysis.study_utils import last_day_of_month
from variables import selected_codelist, start_date, end_date


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
    # calculate how often codes are used
    codes=patients.with_these_clinical_events(
        codelist=selected_codelist,
        between=["index_date", latest_date],
        returning="code",
        return_expectations={"category": {
            "ratios": {str(271649006): 0.6, str(314439003): 0.2, str(314440001): 0.2}},
        },
    ),
    matches=patients.with_these_clinical_events(
        codelist=selected_codelist,
        between=["index_date", latest_date],
        returning="number_of_matches_in_period",
        return_expectations={
                "int": {"distribution": "normal", "mean": 2, "stddev": 0.5}
        },
    ),
)

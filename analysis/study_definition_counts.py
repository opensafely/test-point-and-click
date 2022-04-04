from datetime import date

from cohortextractor import (
    StudyDefinition,
    patients,
    codelist_from_csv,
)

from analysis.study_utils import last_day_of_month


selected_codelist = codelist_from_csv("codelists/opensafely-systolic-blood-pressure-qof.csv",
                                 system="snomed",
                                 column="code",)

start_date = date(year=2020, month=1, day=1)
end_date = date(year=2020, month=12, day=1)

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

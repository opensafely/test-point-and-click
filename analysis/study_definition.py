from datetime import date

from cohortextractor import (
    StudyDefinition,
    patients,
    codelist_from_csv,
)

start_date = "2020-01-01"

selected_codelist = codelist_from_csv("codelists/opensafely-systolic-blood-pressure-qof.csv",
                                 system="snomed",
                                 column="code",)


def calculate_months(selected_codelist):
    months = {}
    for num in range(1, 12):
        start = date.strftime(date(year=2020, month=num, day=1), "%Y-%m-%d")
        end = date.strftime(date(year=2020, month=num+1, day=1), "%Y-%m-%d")
        months[f"month_{num}"] = patients.with_these_clinical_events(
            codelist=selected_codelist,
            between=[start, end],
            returning="binary_flag",
            return_expectations={"date": {"earliest": start, "latest": end}},
        )
    return months


study = StudyDefinition(
    default_expectations={
        "date": {"earliest": start_date, "latest": "today"},
        "rate": "uniform",
        "incidence": 0.5,
    },
    index_date=start_date,
    population=patients.all(),
    **calculate_months(selected_codelist)
)

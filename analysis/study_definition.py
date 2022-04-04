from datetime import date

from cohortextractor import (
    StudyDefinition,
    patients,
    codelist_from_csv,
)

from analysis.study_utils import last_day_of_month, calculate_months


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
    **calculate_months(start_date, end_date, selected_codelist)
)

from datetime import date

from cohortextractor import (
    StudyDefinition,
    patients,
)

from analysis.study_utils import last_day_of_month, calculate_months
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
    **calculate_months(start_date, end_date, selected_codelist)
)

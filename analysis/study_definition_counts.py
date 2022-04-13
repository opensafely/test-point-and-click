from datetime import date, datetime

from cohortextractor import (
    StudyDefinition,
    codelist,
    codelist_from_csv,
    patients,
)

from variables import codelist_file, study_start_date, study_end_date


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


start_date = datetime.strptime(study_start_date, "%Y-%m-%d").date()
end_date = datetime.strptime(study_end_date, "%Y-%m-%d").date()

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
    population=patients.satisfying(
        "currently_registered OR has_died",
        currently_registered=patients.registered_as_of(study_end_date),
        has_died=patients.with_death_recorded_in_primary_care(
            between=[study_start_date, study_end_date], returning="binary_flag"
        ),
    ),
    **calculate_code_frequency(start_date, end_date, selected_codelist),
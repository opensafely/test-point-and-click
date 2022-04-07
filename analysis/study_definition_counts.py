from cohortextractor import (
    StudyDefinition,
    codelist,
    codelist_from_csv,
    patients,
)

from variables import codelist_file


def calculate_code_frequency(selected_codes):
    variables = {}
    for code in selected_codes:
        variables[f"snomed_{code}"] = patients.with_these_clinical_events(
            codelist([code], system="snomed"),
            between=["index_date", "index_date + 1 year"],
            returning="number_of_matches_in_period",
            return_expectations={
                "incidence": 0.1,
                "int": {"distribution": "normal", "mean": 3, "stddev": 1},
            },
        )
    return variables


selected_codelist = codelist_from_csv(
    codelist_file,
    system="snomed",
    column="code",
)

study = StudyDefinition(
    default_expectations={
        "date": {"earliest": "index_date", "latest": "index_date + 1 year"},
        "rate": "uniform",
        "incidence": 0.5,
    },
    index_date="1900-01-01",  # this will be replaced by what's specified in project.yaml
    population=patients.satisfying(
        "currently_registered OR has_died",
        currently_registered=patients.registered_as_of("index_date + 1 year"),
        has_died=patients.with_death_recorded_in_primary_care(
            between=["index_date", "index_date + 1 year"], returning="binary_flag"
        ),
    ),
    **calculate_code_frequency(selected_codelist),
)

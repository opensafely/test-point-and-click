from datetime import date, datetime

from cohortextractor import (
    StudyDefinition,
    codelist,
    patients,
)

codelist_file = "codelists/opensafely-systolic-blood-pressure-qof.csv"

codelist_dict = {
    "bp": "codelists/opensafely-systolic-blood-pressure-qof.csv",
    "eth": "codelists/nhsd-primary-care-domain-refsets-ethnall_cod.csv",
    "aaa": "codelists/nhsd-primary-care-domain-refsets-aaa_cod.csv",
}

study_start_date = "2021-01-01"
study_end_date = "2021-12-31"
frequency = "monthly"
low_count_threshold = 100


def calculate_code_frequency(start_date, end_date, selected_codes):
    start_date_formatted = date.strftime(start_date, "%Y-%m-%d")
    end_date_formatted = date.strftime(end_date, "%Y-%m-%d")

    variables = {}
    for code in selected_codes:
        variables[code] = patients.with_these_clinical_events(
            codelist([code], system="snomed"),
            between=[start_date_formatted, end_date_formatted],
            episode_defined_as="series of events each <= 0 days apart",
            returning="number_of_episodes",
            return_expectations={
                "incidence": 0.1,
                "int": {"distribution": "normal", "mean": 3, "stddev": 1},
            },
        )
    return variables


def build_study_definition_for_counts(codelist):
    start_date = datetime.strptime(study_start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(study_end_date, "%Y-%m-%d").date()

    return StudyDefinition(
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
        **calculate_code_frequency(start_date, end_date, codelist),
    )

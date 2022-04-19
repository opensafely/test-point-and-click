from datetime import date, datetime
from dateutil import rrule

from cohortextractor import (
    codelist_from_csv,
    StudyDefinition,
    patients,
)

from variables import codelist_file


selected_codelist = codelist_from_csv(
    codelist_file,
    system="snomed",
    column="code",
)

study = StudyDefinition(
    default_expectations={
        "date": {"earliest": "index_date", "latest": "last_day_of_month(index_date)"},
        "rate": "uniform",
        "incidence": 0.5,
    },
    index_date="1900-01-01",  # this will be replaced by what's specified in project.yaml
    population=patients.satisfying(
        "currently_registered OR has_died",
        currently_registered=patients.registered_as_of("index_date"),
        has_died=patients.with_death_recorded_in_primary_care(
            between=["index_date", "last_day_of_month(index_date)"], returning="binary_flag"
        ),
    ),
    episodes=patients.with_these_clinical_events(
        codelist=selected_codelist,
        between=["index_date", "last_day_of_month(index_date)"],
        episode_defined_as="series of events each <= 0 days apart",
        returning="number_of_episodes",
        return_expectations={
            "int": {"distribution": "normal", "mean": 2, "stddev": 0.5}
        },
    ),
)

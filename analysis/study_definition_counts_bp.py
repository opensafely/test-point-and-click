from cohortextractor import codelist_from_csv
from variables import build_study_definition_for_counts


selected_codelist = codelist_from_csv(
    "codelists/opensafely-systolic-blood-pressure-qof.csv",
    system="snomed",
    column="code",
)

study = build_study_definition_for_counts(selected_codelist)

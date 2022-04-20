from cohortextractor import codelist_from_csv
from variables import build_study_definition_for_counts


selected_codelist = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-aaa_cod.csv",
    system="snomed",
    column="code",
)

study = build_study_definition_for_counts(selected_codelist)

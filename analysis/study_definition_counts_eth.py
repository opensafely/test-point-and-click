from cohortextractor import codelist_from_csv
from study_utils import build_study_definition_for_counts


selected_codelist = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-ethnall_cod.csv",
    system="snomed",
    column="code",
)

study = build_study_definition_for_counts(selected_codelist)

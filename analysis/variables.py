from datetime import date

from cohortextractor import (
    codelist_from_csv,
)


selected_codelist = codelist_from_csv("codelists/opensafely-systolic-blood-pressure-qof.csv",
                                 system="snomed",
                                 column="code",)

start_date = date(year=2020, month=1, day=1)
end_date = date(year=2020, month=12, day=1)

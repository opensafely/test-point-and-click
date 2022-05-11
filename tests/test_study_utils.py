import pytest
import pandas as pd
import analysis.study_utils as study_utils

@pytest.fixture()
def measure_table():
    """Returns a measures table produced by generate_measures.py."""
    return pd.DataFrame(
        {   
            "date": pd.Series(["2019-01-01", "2019-01-01", "2019-01-01", "2019-02-01","2019-02-01"]),
            "practice": pd.Series([1, 2, 3, 1, 2]),
            "num": pd.Series([3, 10, 1, 0, 4]),
            "list_size": pd.Series([10,20, 4, 2, 8]),
            "value": pd.Series([0,1, 1, 0, 1]),
        }
    )

@pytest.fixture()
def events_count_table():
    """Returns an events code table produced by generate_measures.py."""
    return pd.DataFrame(
        {   
            "count": pd.Series([100, 20, 10]),
            
        }, index=["total_events", "events_in_latest_period", "unique_patients"]
    )     

@pytest.fixture()
def counts_per_code_table():
    """Returns a counts per code table produced by generate_codelist_report.py."""
    return pd.DataFrame(
        {   
            "code": pd.Series(["01", "02", "03"]),
            "num": pd.Series([2, 80, 18])
        }
    )

@pytest.fixture()
def codelist():
    """Returns a codelist like table."""
    return pd.DataFrame(
        {   
            "code": pd.Series(["01", "02", "03"]),
            "term": pd.Series(["code 1", "code 2", "code 3"])
        }
    )




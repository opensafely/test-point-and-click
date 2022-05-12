import pytest
import pandas as pd
from pandas import testing
import study_utils


@pytest.fixture()
def measure_table():
    """Returns a measures table produced by generate_measures.py."""
    return pd.DataFrame(
        {
            "date": pd.Series(
                ["2019-01-01", "2019-01-01", "2019-01-01", "2019-02-01", "2019-02-01"]
            ),
            "practice": pd.Series([1, 2, 3, 1, 2]),
            "num": pd.Series([3, 10, 1, 0, 4]),
            "list_size": pd.Series([10, 20, 4, 2, 8]),
            "value": pd.Series([0, 1, 1, 0, 1]),
        }
    )


@pytest.fixture()
def events_count_table():
    """Returns an events code table produced by generate_measures.py."""
    return pd.DataFrame(
        {
            "count": pd.Series([100, 20, 10]),
        },
        index=["total_events", "events_in_latest_period", "unique_patients"],
    )


top_5_codes_params = [
    # no low numbers
    {
        "obs": {"code": ["01", "02", "03"], "num": [2, 80, 18]},
        "exp": {
            "Code": ["02", "Other"],
            "Description": ["code 2", "-"],
            "Proportion of codes (%)": [80.0, 20.0],
        },
    },
    # all low numbers (and total < threshold)
    {
        "obs": {"code": ["01", "02", "03"], "num": [2, 1, 1]},
        "exp": {"Code": [], "Description": [], "Proportion of codes (%)": []},
    },
    # all low numbers (and total > threshold)
    {
        "obs": {"code": ["01", "02", "03"], "num": [2, 3, 4]},
        "exp": {
            "Code": ["Other"],
            "Description": ["-"],
            "Proportion of codes (%)": [100.0],
        },
    },
    # low numbers with sum > total
    {
        "obs": {"code": ["01", "02", "03"], "num": [4, 4, 10]},
        "exp": {
            "Code": ["03", "Other"],
            "Description": ["code 3", "-"],
            "Proportion of codes (%)": [50.0, 50.0],
        },
    },
    # low numbers with sum < total
    {
        "obs": {"code": ["01", "02", "03"], "num": [2, 2, 10]},
        "exp": {
            "Code": ["Other"],
            "Description": ["-"],
            "Proportion of codes (%)": [100.0],
        },
    },
]


@pytest.fixture()
def codelist():
    """Returns a codelist like table."""
    return pd.DataFrame(
        {
            "code": pd.Series(["01", "02", "03"]),
            "term": pd.Series(["code 1", "code 2", "code 3"]),
        }
    )


@pytest.mark.parametrize("top_5_codes_params", top_5_codes_params)
def test_create_top_5_code_table(top_5_codes_params, codelist):

    # make a counts table
    counts_per_code_table = pd.DataFrame(
        {
            "code": pd.Series(top_5_codes_params["obs"]["code"]),
            "num": pd.Series(top_5_codes_params["obs"]["num"]),
        }
    )

    # make top 5 table using counts table
    obs = study_utils.create_top_5_code_table(
        counts_per_code_table, codelist, "code", "term", 5, 5
    )

    # get expected top 5 table
    exp = pd.DataFrame(
        {
            "Code": pd.Series(top_5_codes_params["exp"]["Code"]),
            "Description": pd.Series(top_5_codes_params["exp"]["Description"]),
            "Proportion of codes (%)": pd.Series(
                top_5_codes_params["exp"]["Proportion of codes (%)"]
            ),
        },
    )

    # below fixes the typing if expected df is empty
    if exp["Code"].empty:
        exp["Code"] = exp["Code"].astype(str)
        exp["Description"] = exp["Description"].astype(str)
        exp["Proportion of codes (%)"] = exp["Proportion of codes (%)"].astype(float)

    testing.assert_frame_equal(obs, exp)

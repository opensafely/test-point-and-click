import pandas as pd
from pathlib import Path
from study_utils import create_top_5_code_table
from variables import codelist_dict, low_count_threshold
import glob
import os

BASE_DIR = Path(__file__).parents[1]
OUTPUT_DIR = BASE_DIR / "output"


def main():
    code_df = pd.read_csv(OUTPUT_DIR / "dummy/counts_per_code.csv")
    codelist = pd.read_csv(codelist_dict["bp"])

    top_5_code_table = create_top_5_code_table(
        df=code_df,
        code_df=codelist,
        code_column="code",
        term_column="term",
        low_count_threshold=low_count_threshold,
    )
    top_5_code_table.to_csv(OUTPUT_DIR / f"top_5_code_table_{s}.csv", index=False)


if __name__ == "__main__":
    main()

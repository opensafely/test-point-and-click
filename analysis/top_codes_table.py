import pandas as pd
from pathlib import Path
from study_utils import create_top_5_code_table

BASE_DIR = Path(__file__).parents[1]
OUTPUT_DIR = BASE_DIR / "output"

# codelist used for measure
codelist = pd.read_csv('codelists/opensafely-systolic-blood-pressure-qof.csv', dtype={"code": str})

def main():
    df = pd.read_csv(OUTPUT_DIR / "input_counts.csv")
    top_5_code_table = create_top_5_code_table(df=df, code_df=codelist, code_column='code', term_column='term')
    top_5_code_table.to_csv(OUTPUT_DIR / 'top_5_code_table.csv', index=False)

if __name__ == "__main__":
    main()
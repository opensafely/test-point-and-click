import pandas as pd
from pathlib import Path
from study_utils import create_top_5_code_table
from variables import codelist_file, low_count_threshold

BASE_DIR = Path(__file__).parents[1]
OUTPUT_DIR = BASE_DIR / "output"

# codelist used for measure
codelist = pd.read_csv(codelist_file)

def main():
    df = pd.read_feather(OUTPUT_DIR / "input_counts.feather")
    top_5_code_table = create_top_5_code_table(df=df, code_df=codelist, code_column='code', term_column='term', low_count_threshold=low_count_threshold)
    top_5_code_table.to_csv(OUTPUT_DIR / 'top_5_code_table.csv', index=False)

if __name__ == "__main__":
    main()
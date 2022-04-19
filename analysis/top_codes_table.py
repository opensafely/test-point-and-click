import pandas as pd
from pathlib import Path
from study_utils import create_top_5_code_table
from variables import codelist_dict, low_count_threshold
import glob 
import os
BASE_DIR = Path(__file__).parents[1]
OUTPUT_DIR = BASE_DIR / "output"


def main():
    for path in glob.glob(os.path.join(OUTPUT_DIR, "input_counts_*.feather")):
        df = pd.read_feather(path)                                                                                                                                                                                                                                 
        # fetch codelist used for measure
        s = path[:path.index(".")].partition("_")[2].partition("_")[2]
        codelist = pd.read_csv(codelist_dict[s])
        top_5_code_table = create_top_5_code_table(df=df, code_df=codelist, code_column='code', term_column='term', low_count_threshold=low_count_threshold)
        top_5_code_table.to_csv(OUTPUT_DIR / f'top_5_code_table_{s}.csv', index=False)

if __name__ == "__main__":
    main()

import pandas as pd
from pathlib import Path
#from study_utils import create_top_5_code_table
import glob 
import os
BASE_DIR = Path(__file__).parents[1]
OUTPUT_DIR = BASE_DIR / "output"


def main():
    out = pd.DataFrame(columns=["episodes", "patient_id"])
    for path in glob.glob(os.path.join(OUTPUT_DIR, "input_weekly_*.feather")):
        df = pd.read_feather(path)   
        date = path.split("_")[-1].replace(".feather","")         

        # sum episodes and count patients
        out0 = df.loc[df["episodes"]>0].agg({"episodes":"sum", "patient_id":"count"})

        #add results to output table
        out.loc[date] = out0                                                                                                                                                                                                           
        
    out.to_csv(OUTPUT_DIR / f'weekly_count.csv', index=True)

if __name__ == "__main__":
    main()

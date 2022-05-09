import random
from datetime import date, timedelta
from pathlib import Path
import pandas as pd
import numpy as np

random.seed(123)


Path("output/dummy").mkdir(parents=True, exist_ok=True)

rows = []
rows_list_size = []

for code in range(16):
    for date_offset in range(70):
        for practice in range(100):
            jitter = random.uniform(0.8, 1.2)
            count = int(
                (1000 + practice * jitter - 5 * abs(date_offset - 100))
                * jitter
                * 1.595**-code
            )
            rows.append(
                [
                    f"{code:02x}" * 6,
                    date(2022, 1, 1) + timedelta(date_offset),
                    f"{practice:02}",
                    count,
                ]
            )


for practice in range(100):
    rows_list_size.append([f"{practice:02}", int(random.gauss(2000, 500))])

counts = pd.DataFrame(rows, columns=["code", "date", "practice", "num"])
counts["date"] = pd.to_datetime(counts["date"])

counts_per_code = counts.groupby("code")["num"].sum()
counts_per_code.to_csv("output/dummy/counts_per_code.csv")

grouper = pd.Grouper(key="date", freq="W-MON")
counts_per_week = counts.groupby(["practice", grouper])["num"].sum()
counts_per_week.to_csv("output/dummy/counts_per_week_per_practice.csv")

list_size = pd.DataFrame(rows_list_size, columns=["practice", "list_size"])
list_size.to_csv("output/dummy/list_sizes.csv", index=False)
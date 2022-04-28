import pandas as pd

counts_table = pd.read_csv("output/dummy/counts_per_week.csv")

counts_table.rename(columns={"num": "value"}, inplace=True)

counts_table.to_csv("output/dummy/measure_counts_per_week.csv", index=False)

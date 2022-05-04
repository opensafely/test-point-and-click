import pandas as pd
from study_utils import calculate_rate

counts_table = pd.read_csv("output/counts_per_week_per_practice.csv")
list_sizes = pd.read_csv("output/list_sizes.csv")

counts_table = counts_table.merge(list_sizes, on=["practice"], how="inner")
counts_table["value"] = counts_table["num"] / counts_table["list_size"]
counts_table["value"] = calculate_rate(counts_table, "value", round_rate=True)

counts_table.to_csv("output/measure_counts_per_week_per_practice.csv", index=False)

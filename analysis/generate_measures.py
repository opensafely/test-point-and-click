import pandas as pd
import json
from study_utils import calculate_rate
from variables import frequency

counts_table = pd.read_csv("output/dummy/counts_per_week_per_practice.csv", parse_dates=["date"])
list_sizes = pd.read_csv("output/dummy/list_sizes.csv")

counts_table = counts_table.merge(list_sizes, on=["practice"], how="inner")
counts_table["value"] = counts_table["num"] / counts_table["list_size"]
counts_table["value"] = calculate_rate(counts_table, "value", round_rate=True)

counts_table.to_csv("output/measure_counts_per_week_per_practice.csv", index=False)

# count total number of events
event_counts = {}
event_counts["total_events"] = int(counts_table["num"].sum())


# total events in last week/month
latest_time_period = counts_table["date"].max()
event_counts["events_in_latest_period"] = int(counts_table.loc[counts_table["date"] == latest_time_period, "num"].sum())


with open(f"output/event_counts.json", "w") as f:
    json.dump(event_counts, f)






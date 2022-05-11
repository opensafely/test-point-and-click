import pandas as pd
import numpy as np
from study_utils import calculate_rate, round_values, drop_irrelevant_practices
from variables import low_count_threshold, rounding_base

counts_table = pd.read_csv(
    "output/counts_per_week_per_practice.csv", parse_dates=["date"]
)
list_sizes = pd.read_csv("output/list_sizes.csv")

counts_table = counts_table.merge(list_sizes, on=["practice"], how="inner")
counts_table["value"] = counts_table["num"] / counts_table["list_size"]
counts_table["value"] = calculate_rate(counts_table, "value", round_rate=True)

practice_count_total = len(np.unique(counts_table["practice"]))
#drop practices with no events for entire period
counts_table = drop_irrelevant_practices(counts_table)

practice_count_subset = len(np.unique(counts_table["practice"]))

practice_count = pd.DataFrame(
    {
        "total": practice_count_total,
        "with_at_least_1_event": practice_count_subset
    },
    index=["count"],
)
practice_count.T.to_csv("output/practice_count.csv")


counts_table.to_csv("output/measure_counts_per_week_per_practice.csv", index=False)

# count total number of events

total_events = int(counts_table["num"].sum())


# total events in last week/month
latest_time_period = counts_table["date"].max()
events_in_latest_period = int(
    counts_table.loc[counts_table["date"] == latest_time_period, "num"].sum()
)

events_counts = pd.DataFrame(
    {
        "total_events": total_events,
        "events_in_latest_period": events_in_latest_period,
        "unique_patients": np.nan,
    },
    index=["count"],
)


events_counts = events_counts.T

# redact low counts
events_counts[events_counts <= low_count_threshold] = f"<={low_count_threshold}"


# round
events_counts["count"] = events_counts["count"].apply(
    lambda x: round_values(x, base=rounding_base)
)

events_counts.to_csv("output/event_counts.csv")

import pandas as pd
import numpy as np
from dateutil import relativedelta


def last_day_of_month(dt):
    return dt + relativedelta.relativedelta(day=31)


def last_day_of_week(dt):
    return dt + relativedelta.relativedelta(day=7)


def group_low_values(df, count_column, code_column, threshold):
    """Suppresses low values and groups suppressed values into
    a new row "Other".

    Args:
        df: A measure table of counts by code.
        count_column: The name of the count column in the measure table.
        code_column: The name of the code column in the codelist table.
        threshold: Redaction threshold to use
    Returns:
        A table with redacted counts
    """

    # get sum of any values <= threshold
    suppressed_count = df.loc[df[count_column] <= threshold, count_column].sum()

    # if no values are suppressed we don't need to do anything
    if suppressed_count == 0:
        pass

    # if suppressed values >0 ensure total suppressed count > threshold
    else:
        # redact counts <= threshold
        df.loc[df[count_column] <= threshold, count_column] = np.nan

        # if suppressed count <= threshold redact further values
        while suppressed_count <= threshold:
            suppressed_count += df[count_column].min()
            df.loc[df[count_column].idxmin(), :] = np.nan

        # drop all rows where count column is null
        df = df.loc[df[count_column].notnull(), :]

        # add suppressed count as "Other" row (if > threshold)
        if suppressed_count > threshold:
            suppressed_count = {"code": "Other", "count": suppressed_count}
            df = df.append(suppressed_count, ignore_index=True)

    return df


def create_top_5_code_table(
    df, code_df, code_column, term_column, low_count_threshold, nrows=5
):
    """Creates a table of the top 5 codes recorded with the number of events and % makeup of each code.
    Args:
        df: A measure table.
        code_df: A codelist table.
        code_column: The name of the code column in the codelist table.
        term_column: The name of the term column in the codelist table.
        measure: The measure ID.
        low_count_threshold: Value to use as threshold for disclosure control.
        nrows: The number of rows to display.
    Returns:
        A table of the top `nrows` codes.
    """

    # sum event counts over patients
    event_counts = (
        df.sum()
        .drop("patient_id")
        .rename_axis(code_column)
        .reset_index(name="Count")
        .sort_values(ascending=False, by="Count")
    )

    event_counts = group_low_values(
        event_counts, "Count", code_column, low_count_threshold
    )

    # calculate % makeup of each code
    total_events = event_counts["Count"].sum()
    event_counts["Proportion of codes (%)"] = round(
        (event_counts["Count"] / total_events) * 100, 2
    )

    # Gets the human-friendly description of the code for the given row
    # e.g. "Systolic blood pressure".
    code_df[code_column] = code_df[code_column].astype(str)
    code_df = code_df.set_index(code_column).rename(
        columns={term_column: "Description"}
    )

    event_counts = event_counts.set_index(code_column).join(code_df).reset_index()

    # set description of "Other column" to something readable
    event_counts.loc[event_counts[code_column] == "Other", "Description"] = "-"

    # Rename the code column to something consistent
    event_counts.rename(columns={code_column: "Code"}, inplace=True)

    # drop events column
    event_counts = event_counts.loc[
        :, ["Code", "Description", "Proportion of codes (%)"]
    ]

    # return top n rows
    return event_counts.head(5)

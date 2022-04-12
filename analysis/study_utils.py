import pandas as pd
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

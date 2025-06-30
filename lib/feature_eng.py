import pandas as pd
import numpy as np


def find_common_columns(feature_cols=[], df_cols=[]):
    """
    Check for common columns from two lists

    Args:
        fature_cols (list): First list of values (can contain any types)
        df_cols (list): Second list of values (can contain any types)

    Returns:
        list: A list of feature columns presente on the dataframe
    """
    df_cols_list = list(df_cols) if hasattr(df_cols, "__iter__") else []
    common = {col for col in feature_cols if col in df_cols_list}

    return common


def find_class_columns(feature_cols=[], file_list=[]):
    """
    Find common columns from two lists of files.

    Given a list of columns and a list of files, this function will return a dictionary
    with the common columns for each file.

    Args:
        feature_cols (list): First list of values (can contain any types)
        file_list (list): Second list of values (can contain any types)

    Returns:
        dict: A dictionary with the common columns for each file.
    """
    result = {}
    for file in file_list:
        df = pd.read_csv(f"data/csv_files/train/{file}.csv", nrows=0, header=0)
        commum_cols = find_common_columns(feature_cols=feature_cols, df_cols=df.columns)
        if commum_cols:
            result[file] = commum_cols
    return result


def create_pivot_table(df_base, csv_file, cls):
    """
    Create a pivot table for a given class column.

    Args:
        df_base (pd.DataFrame): Base dataframe with 'case_id' and 'target' columns.
        csv_file (str): Path to csv file with 'case_id' and class column.
        cls (str): Class column name.

    Returns:
        pd.DataFrame: A pivot table with the 'target' column as values, and the class column as index.
    """
    df_static = pd.read_csv(csv_file, usecols=["case_id", cls])
    df_base_class = pd.merge(df_base, df_static, how="left", on="case_id")
    df_base_class.fillna(0, inplace=True)
    df_process = (
        df_base_class.groupby(cls)["target"].value_counts().unstack(fill_value=0)
    )
    return df_process


def calculate_woe_iv(pivot_table):
    pivot_table["pct_non_default"] = pivot_table[0] / pivot_table[0].sum()
    pivot_table["pct_default"] = pivot_table[1] / pivot_table[1].sum()
    pivot_table["woe"] = np.log(
        pivot_table["pct_non_default"] / pivot_table["pct_default"]
    )
    pivot_table["iv"] = (
        pivot_table["pct_non_default"] - pivot_table["pct_default"]
    ) * pivot_table["woe"]
    return pivot_table


def create_iv_pivot_table_with_binning(df_base, csv_file, cls, num_bins=10):
    """
    Create a pivot table with binning and calculate WOE/IV metrics.

    This function takes a base dataframe, a CSV file path, and a specified class column.
    It merges the data, creates quantile-based bins for the class column, and computes
    Weight of Evidence (WOE) and Information Value (IV) metrics for each bin.

    Args:
        df_base (pd.DataFrame): Base dataframe with 'case_id' and 'target' columns.
        csv_file (str): Path to the CSV file containing 'case_id' and the class column.
        cls (str): The name of the class column to bin and analyze.
        num_bins (int, optional): Number of quantile bins to create. Defaults to 10.

    Returns:
        pd.DataFrame: A pivot table with binned ranges, non-default and default counts,
                      and WOE/IV metrics for each bin.
    """

    df_static = pd.read_csv(csv_file, usecols=["case_id", cls])
    df_merged = pd.merge(df_base, df_static, how="left", on="case_id").fillna(0)

    # Create quantile bins and generate clean labels
    df_merged[f"{cls}_binned"], bins = pd.qcut(
        df_merged[cls], q=num_bins, duplicates="drop", precision=0, retbins=True
    )

    # Reassign with formatted labels
    bin_labels = [f"{int(bins[i])}-{int(bins[i+1])}" for i in range(len(bins) - 1)]
    df_merged[f"{cls}_binned"] = pd.qcut(
        df_merged[cls], q=num_bins, labels=bin_labels, duplicates="drop"
    )

    # Create pivot table
    pivot_table = (
        df_merged.groupby(f"{cls}_binned")["target"]
        .value_counts()
        .unstack(fill_value=0)
    )

    # Calculate metrics
    pivot_table["non_events"] = pivot_table[0] / pivot_table[0].sum()
    pivot_table["events"] = pivot_table[1] / pivot_table[1].sum()
    pivot_table["woe"] = np.log(pivot_table["non_events"] / pivot_table["events"])
    pivot_table["iv"] = (
        pivot_table["non_events"] - pivot_table["events"]
    ) * pivot_table["woe"]

    # Reset index for cleaner output and rename columns
    pivot_table = pivot_table.reset_index().rename(
        columns={f"{cls}_binned": "Bin_Range", 0: "Non_Default", 1: "Default"}
    )
    return pivot_table

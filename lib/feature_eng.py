import pandas as pd

def find_common_columns(feature_cols=[], df_cols=[]):
    """
    Check for common columns from two lists
    
    Args:
        fature_cols (list): First list of values (can contain any types)
        df_cols (list): Second list of values (can contain any types)
        
    Returns:
        list: A list of feature columns presente on the dataframe
    """
    df_cols_list = list(df_cols) if hasattr(df_cols, '__iter__') else []
    common = {col for col in feature_cols if col in df_cols_list}
  
    return common

def find_class_columns(feature_cols=[], file_list=[]):
    result = {}
    for file in file_list:
        df = pd.read_csv(f'data/csv_files/train/{file}.csv', nrows=0, header=0)
        commum_cols = find_common_columns(feature_cols=feature_cols, df_cols=df.columns)
        if commum_cols:
            result[file] = commum_cols
    return result

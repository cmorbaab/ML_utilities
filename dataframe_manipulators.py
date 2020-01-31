import pandas as pd 
import numpy as np 
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder
import re

"""
"""

def encode_ordinal(df, column_name, category_order=None):
    """Encodes ordinal features (implied order, ex. t-shirt size). Pass a list to category_order in order to specify the order of the encoding. Not in place.
    
    Arguments:
        df {pandas DataFrame} -- the dataframe to be manipulated
        column_name {string} -- the name of the column to be manipulated
    
    Keyword Arguments:
        category_order {list} -- the list containing a pre-defined ordering of the column values (ex. [small, medium, large]) (default: {None})

    Returns:
        a copy of the manipulated dataframe
    """
    if category_order:
        encoder = OrdinalEncoder(categories=category_order)
    else:
        encoder = OrdinalEncoder()

    transformed_column = encoder.fit_transform(df[column_name].values.reshape(-1, 1))

    df_copy = df.copy()
    df_copy[column_name] = transformed_column
    return df_copy

def encode_nominal(df, column_name, binary=False):
    """Encodes nominal features (no implied order, ex. colors) through one-hot encoding. If binary = True (only 2 unique values) do encoding in one column.
    
    Arguments:
        df {pandas dataframe} -- the dataframe to be manipulated
        column_name {string} -- the name of the column to be manipulated
    
    Keyword Arguments:
        binary {bool} -- true = the column is binary, false = the column is not binary (default: {False})
    
    Returns:
        a copy of the manipulated dataframe
    """
    if binary:
        mapping = {}
        unique = set(df[column_name].unique())
        if len(unique) != 2:
            raise ValueError("The column specified is not a binary column.")

        for i, e in enumerate(unique):
            mapping[e] = i

        encoded_column = df[column_name].map(mapping)

        df_copy = df.copy()
        df_copy[column_name] = encoded_column
        return df_copy
    else:
        column_index = df.columns.get_loc(column_name)
        #pd.get_dummies does not manipulate the original df object
        df_new = pd.get_dummies(data=df, columns=[column_name])
        return df_new

def encode_regex(df, column_name, regex_mapping):
    """Encodes features with regular expression.
    
    Arguments:
        df {pandas dataframe} -- the dataframe to be manipulated
        column_name {string} -- the name of the column to be manipulated 
        regex_mapping {dict} -- a dictionary w/ key = the regular expression, value = value to be encoded. Regular exp. should not overlap.
    
    Returns:
        a copy of the manipulated dataframe
    """
    # compiled the regex to increase speed
    regex_mapping_comp = {re.compile(k) : v for k, v in regex_mapping.items()}
    def map_regex(item):
        # convert item type to string to apply regex
        item = str(item)
        item_mapped = None
        for pattern, v in regex_mapping_comp.items():
            if pattern.search(item):
                item_mapped = v

        return item_mapped

    df_copy = df.copy()
    df_copy[column_name] = list(map(map_regex, df_copy[column_name]))
    return df_copy

def encode_class_label(df, column_name):
    """Encode class labels (order does not matter)
    
    Arguments:
        df {pandas dataframe} -- the dataframe to be manipulated
        column_name {string} -- the name of the column (class label) to be manipulated
    
    Returns:
        [pandas dataframe] -- a manipulated copy of the passed in dataframe
    """
    df_copy = df.copy()
    class_mapping = {label: idx for idx,label in enumerate(np.unique(df_copy[column_name]))}
    df_copy[column_name] = df_copy[column_name].map(class_mapping)
    return df_copy

def fill_NaN_column(df, column_name, fill_value):
    """Fills any nan values in the specified column with the passed fill_value
    
    Arguments:
        df {pandas dataframe} -- the df to be manipulated
        column_name {string} -- the name of the column to be manipulated
        fill_value {obj} -- the fill value for any nan in the column
    
    Returns:
        pandas dataframe -- a manipulated copy of the dataframe
    """
    df_copy = df.copy() 
    df_copy[column_name] = df_copy[column_name].fillna(fill_value, inplace=False)
    return df_copy

def impute_NaN_column(df, column_name, strategy):
    """ Impute the nans of a specified column using various strategies

    Arguments:
        df {pandas datafram} -- the dataframe to be manipulated
        column_name {string} -- the name of the column to be manipulated
        strategy {string} -- the name of the specified column
    
    Raises:
        ValueError: error for trying to get the mean of a non-numeric column
        ValueError: error for trying to get the median of a non-numeric column
        ValueError: error for specifying an incorrect strategy
    
    Returns:
        [type] -- [description]
    """
    df_copy = df.copy()
    # Impute one column
    if strategy == "mean":
        # if column is non numeric raise error. Cannot get mean of a numeric column
        if not np.issubdtype(df[column_name].dtype, np.number):
            raise ValueError("Cannot compute mean of a non-numeric column")
        df_copy[column_name].fillna(df_copy[column_name].mean(), inplace=True)
    elif strategy == "most_frequent":
        # dropna=True means to not consider NaN values in computing the mode
        df_copy[column_name].fillna(df_copy[column_name].mode(dropna=True).iloc[0], inplace=True)
    elif strategy == "median":
        # if column is non numeric raise error. Cannot get median of a numeric column
        if not np.issubdtype(df[column_name].dtype, np.number):
            raise ValueError("Cannot compute median of a non-numeric column")
        df_copy[column_name].fillna(df_copy[column_name].median(), inplace=True)
    else:
        raise ValueError("Strategy \'" + strategy + "\' is not a valid strategy.")
    
    return df_copy

df = pd.read_csv("Sample_Data/happy_one_versus_all.csv", index_col=0)
# print(df["track_label"].unique())
# df_new = encode_class_label(df, "track_label")
# print(df_new["track_label"].unique())
# print(df["track_label"].unique())


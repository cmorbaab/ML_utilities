import pandas as pd 
import numpy as np 
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder

"""
"""

def encode_ordinal(df, column_name, category_order=None):
    """Encodes ordinal features (implied order, ex. t-shirt size). Pass a list to category_order in order to specify the order of the encoding. Not in place.
    
    Arguments:
        df {pandas DataFrame} -- the dataframe to be manipulated
        column_name {string} -- the name of the column to be manipulated
    
    Keyword Arguments:
        category_order {list} -- the list containing a pre-defined ordering of the column values (ex. [small, medium, large]) (default: {None})
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


# TODO: Regex mapper 

df = pd.read_csv("Sample_Data/happy_one_versus_all.csv", index_col=0)
df = encode_nominal(df, "explicit", binary=False)

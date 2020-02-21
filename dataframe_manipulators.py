import pandas as pd 
import numpy as np 
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder
import re
import time
from datetime import date

class manipulator:
    def __init__(self, function, args):
        self.function = function
        self.args = args
    
    def do(self, df):
        df_copy = df.copy()
        temp = [df_copy] + self.args
        df_manipulated = self.function(*temp)
        return df_manipulated

    def get_function(self):
        return self.function

    def get_args(self):
        return self.args

        
def drop_columns(df, column_names):
    """Drop columns from dataframe
    
    Arguments:
        df {pandas dataframe} -- the dataframe to be manipulated
        column_names {list of strings} -- a list of the names of the columns to be dropped
    
    Returns:
        pandas dataframe -- a manipulated copy of the pandas dataframe
    """
    if type(column_names)!=list:
        raise TypeError("Column names object needs to be a list of strings")

    df_copy = df.copy()
    df_copy.drop(column_names, axis=1, inplace=True)
    return df_copy

def drop_rows(df, row_indices):
    """Drop rows from dataframe
    
    Arguments:
        df {pandas dataframe} -- the dataframe to be manipulated
        row_indices {list} -- a list of the indices of the rows to be dropped
    
    Returns:
        pandas dataframe -- a manipulated copy of the pandas dataframe
    """
    if type(row_indices)!=list:
        raise TypeError("Row indices object needs to be a list of strings")

    df_copy = df.copy()
    df_copy.drop(row_indices, axis=0, inplace=True)
    return df_copy

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

def handle_date(df, column_name):
    """Handle date values. Works for dates in format year-month-day, but needs at least the year. TODO generalize 
    
    Arguments:
        df {pandas dataframe} -- the dataframe to manipulated
        column_name {string} -- the name of the date column to be manipulated
    
    Raises:
        ValueError: raises error if date values are not in correct format
    
    Returns:
        pandas dataframe -- a manipulated copy of the passed in dataframe
    """
    def convert_date_to_date_list(date_str):
        if len(date_str) == 10:
            # contains year-month-day
            date_obj = date(year=int(date_str[0:4]), month=int(date_str[5:7]), day=int(date_str[8:10]))
            date_list = [date_obj.year, (date_obj.month-1)//3, date_obj.month, date_obj.weekday(), date_obj.day, date_obj.strftime('%j')]
            date_list = [int(x) for x in date_list]
        elif len(date_str) == 7:
            # contains year-month
            date_list = [int(date_str[0:4]), (int(date_str[5:7]) - 1)//3, int(date_str[5:7]), np.nan, np.nan, np.nan]
        elif len(date_str) == 4:
            # contains year
            date_list = [int(date_str[0:4]), np.nan, np.nan, np.nan, np.nan, np.nan]
        else:
            raise ValueError("Invalid Date Input on Date:" + date_str)

        return date_list

    df_copy = df.copy()
    #create new columns in df  
    new_col_names = ["_year", "_quarter", "_month", "_day_of_week", "_day_of_month", "_day_of_year"]
    new_col_names = [column_name + x for x in new_col_names]
    new_col_values = [[] for _ in range(6)]
    # for each row, get date and then get new date values and apply it to the df
    date_col_index = df_copy.columns.get_loc(column_name)
    for row in df_copy.iterrows():
        date_str = row[1][date_col_index]
        date_list = convert_date_to_date_list(date_str)
        for j, val in enumerate(date_list):
            new_col_values[j].append(val)

    for i, new_col in enumerate(new_col_names):
        df_copy[new_col] = new_col_values[i]

    df_copy.drop([column_name], inplace=True, axis=1)
    return df_copy



# df = pd.read_csv("Sample_Data/excited_tracks.csv", index_col=0)

# man = manipulator(handle_date, ["release_date"])
# df = man.do(df)
# print(df.columns.values)


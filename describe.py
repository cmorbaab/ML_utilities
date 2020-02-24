import pandas as pd 
import numpy as np 
import time
from constants import *
"""
describe(df):
    prints out a description of the df. Goes column by column displaying the object type, unique values, and the recommended encoding method.
"""

def describe(df):
    """
    TODO: Check duplicate indices
    """
    # Describe Dataframe shape **************************************************************************************************************************************************
    num_rows = df.shape[0]
    num_columns = df.shape[1]
    print("{}Dataframe Shape:{}".format(bcolors.UNDERLINE, bcolors.ENDC))
    print("\t{}{} rows{} and {}{} columns{}.".format(bcolors.YELLOW, num_rows, bcolors.ENDC, bcolors.YELLOW, num_columns, bcolors.ENDC))

    # Describe Dataframe Rows *************************************************************************************************************************************************
    print("{}Dataframe Rows:{}".format(bcolors.UNDERLINE, bcolors.ENDC))
    print("\t{}{}{}".format(bcolors.PURPLE, "Missing Values:", bcolors.ENDC))
    # now do rows
    # nan count --> [] of row indices
    row_nan_count_dict = {}
    for index, row in df.iterrows():
        nan_count = row.isnull().sum()
        index_list = row_nan_count_dict.get(nan_count, None)
        if index_list:
            # if value already exists append the index to the list
            row_nan_count_dict[nan_count] = index_list.append(index)
        else:
            # if value does not exist create a new list
            new_index_list = [index]
            row_nan_count_dict[nan_count] = new_index_list

    # 50% + rows:
    fifty_plus_count = 0
    fifty_perc_rows = int(num_rows*thresholds.FIFTY_MISSING)
    hund_perc_rows = int(num_rows*thresholds.ALL_MISSING)
    for i in range(fifty_perc_rows, hund_perc_rows):
        fifty_plus_count += len(row_nan_count_dict.get(i, []))

    # 25%-50% rows:
    twenty_five_count = 0
    twenty_five_perc_rows = int(num_rows*thresholds.TWENTY_FIVE_MISSING)
    for i in range(twenty_five_perc_rows, fifty_perc_rows):
        twenty_five_count += len(row_nan_count_dict.get(i, []))

    # 10%-25% rows:
    ten_count = 0
    ten_perc_rows = int(num_rows*thresholds.TEN_MISSING)
    for i in range(ten_perc_rows, twenty_five_perc_rows):
        ten_count += len(row_nan_count_dict.get(i, []))

    header = "Num of rows w/ 50%+ values missing:".ljust(print_pref.PADDING_COLUMN, ' ')
    print("\t\t{}{}{}{}".format(header, bcolors.YELLOW, fifty_plus_count, bcolors.ENDC))

    header = "Num of rows w/ 25%-50% values missing:".ljust(print_pref.PADDING_COLUMN, ' ')
    print("\t\t{}{}{}{}".format(header, bcolors.YELLOW, twenty_five_count, bcolors.ENDC))

    header = "Num of rows w/ 10%-25% values missing:".ljust(print_pref.PADDING_COLUMN, ' ')
    print("\t\t{}{}{}{}".format(header, bcolors.YELLOW, ten_count, bcolors.ENDC))


    # Describe the Dataframes columns *******************************************************************************************************************************************
    print("{}Dataframe Columns:{}".format(bcolors.UNDERLINE, bcolors.ENDC))
    for column_name in df.columns.values:
        print("\t{}{}:{}".format(bcolors.BLUE, column_name, bcolors.ENDC))

        # Print column value type
        header = "Value type:".ljust(print_pref.PADDING_COLUMN, ' ')
        dtype = df[column_name].dtype
        print("\t\t{}{}{}{}".format(header, bcolors.YELLOW, dtype, bcolors.ENDC))

        # Print number of unique values in df
        header = "Number of unique values: ".ljust(print_pref.PADDING_COLUMN, ' ')
        unique_values = set(df[column_name].unique())
        num_uniques = len(unique_values)
        print("\t\t{}{}{}{}".format(header, bcolors.YELLOW, num_uniques, bcolors.ENDC))

        # Print predicted column type
        header = "Predicted column type:".ljust(print_pref.PADDING_COLUMN, ' ')
        pred_column_type = get_pred_column_type(unique_values, num_rows)
        print("\t\t{}{}{}{}".format(header, bcolors.YELLOW, pred_column_type, bcolors.ENDC))

        # Print a "sneak peek" into unqiue values
        header = "Preview unique values:".ljust(print_pref.PADDING_COLUMN, ' ')
        # get first 3 unique values --> preview. Max number of uniques shown is set by MAX_NUMBER_UNIQUE_PREVIEW_SHOWN. However, if a variable's string size is greater than 
        # MAX_LENGTH_UNIQUE_PREVIEW, then stop printing values
        unique_preview = set()
        i = 1
        for elem in unique_values:
            unique_preview.add(elem)
            if i >= print_pref.MAX_NUMBER_UNIQUE_PREVIEW_SHOWN:
                break
            elif len(str(elem)) >= print_pref.MAX_LENGTH_UNIQUE_PREVIEW:
                break
            i+= 1
        print("\t\t{}{}{}{}".format(header, bcolors.YELLOW, unique_preview, bcolors.ENDC))

        # Print number of missing values
        nan_count = df[column_name].isna().sum()
        nan_percent = (float(nan_count)/num_rows)*100
        header = "Number of nan values:".ljust(print_pref.PADDING_COLUMN, ' ')
        print("\t\t{}{}{}{}".format(header, bcolors.YELLOW, nan_count, bcolors.ENDC))

        # Print percent of rows are missing values in this column
        header = "% of rows with nan values:".ljust(print_pref.PADDING_COLUMN, ' ')
        print("\t\t{}{}{}{}".format(header, bcolors.YELLOW, round(nan_percent,4), bcolors.ENDC))

        # Print whether a column is clean or not
        header = "Is column clean?:".ljust(print_pref.PADDING_COLUMN, ' ')
        is_clean = is_column_clean(df[column_name])
        if is_clean:
            print("\t\t{}{}{}{}{}".format(bcolors.UNDERLINE, header, bcolors.GREEN, "YES {}".format(print_pref.CHECKMARK), bcolors.ENDC))
        else:
            print("\t\t{}{}{}{}{}".format(bcolors.UNDERLINE, header, bcolors.RED, "NO {}".format(print_pref.CROSSMARK), bcolors.ENDC))





        
def get_pred_column_type(unique_values_set, number_rows):
    if len(unique_values_set) == thresholds.UNARY:
        return "UNARY"
    elif len(unique_values_set) == thresholds.BINARY:
        return "BINARY"
    elif len(unique_values_set) == thresholds.PURE_UNIQUE*number_rows:
        return "PURE UNIQUE"
    elif len(unique_values_set) >= thresholds.NINETY_UNIQUE*number_rows:
        return "90% UNIQUE"
    elif len(unique_values_set) >= thresholds.FIFTY_UNIQUE*number_rows:
        return "50% UNIQUE"
    else:
        return "NONE"

def is_column_clean(column):
    """
    Given a column (series) as input checks that the column has numerical values and contains no nulls
    Output: 0 = Not clean, 1 = Clean
    """
    # check that column is numeric
    is_numeric = np.issubdtype(column.dtype, np.number)
    # check that column has no NAN
    contains_nulls = column.isnull().values.any()

    return is_numeric and not contains_nulls

# start_time = time.time()

# print("--- %s seconds ---" % (time.time() - start_time))

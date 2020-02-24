# Constants:

class print_pref:
    PADDING_COLUMN = 30
    # Max number of unique values displayed
    MAX_NUMBER_UNIQUE_PREVIEW_SHOWN = 3
    # Max size of unique value displayed (characters)
    MAX_LENGTH_UNIQUE_PREVIEW = 15
    CHECKMARK = u'\u2713'
    CROSSMARK = u'\u2717'

class bcolors:
    # purple for rows
    PURPLE = '\033[95m'
    # blue for cols
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class thresholds:
    # column values is unqiue per each sample
    PURE_UNIQUE = 1.0
    # column values is unqiue for more than 90% of samples
    NINETY_UNIQUE = 0.9
    # column values are unique for more than 50% of samples
    FIFTY_UNIQUE = 0.5
    # column with only 2 values
    BINARY = 2
    # column with only 1 value
    UNARY = 1
    # rows/columns with all values missings
    ALL_MISSING = 1.0
    # rows/columns with more than 50% of values missing
    FIFTY_MISSING = 0.5
    # rows/columns with 25-50% of values missing
    TWENTY_FIVE_MISSING = 0.25
    # rows/columns with 10-25% of values missing
    TEN_MISSING = 0.10
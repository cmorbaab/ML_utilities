import dataframe_manipulators as manip
import dataframe_describe as describe


class dataframe_preprocessor:
    def __init__(self, _df):
        self.df = _df

    def describe():
        describe.describe_df(self.df)


df = pd.read_csv("Sample_Data/excited_tracks.csv", index_col=0)
obj = dataframe_preprocessor(df)
obj.describe()
        
from manipulator import *
import describe as describe
import pandas as pd


class preprocessor:
    def __init__(self, df):
        self.df = df.copy()
        self.manipulations = []

    def __str__(self):
        out = "Preprocessor Object:" 
        for i, manipulation in enumerate(self.manipulations):
            out+= "\n\t{} -- {}".format(i+1, manipulation)
        
        return out

    def describe(self):
        describe.describe(self.df)

    def preprocess(self):
        """Preprocess/Clean the dataframe by doing each of the manipulation operations. Returns a copy
        
        Returns:
            pandas dataframe -- a copy of the manipulated dataframe
        """
        df_copy = df.copy()
        for manipulation in self.manipulations:
            df_copy = manipulation.do(df_copy)
        return df_copy
    
    def get_manipulations(self):
        return self.manipulations 
    
    def append_manipulation(self, manipulation):
        self.manipulations.append(manipulation)

    def get_manipulation_names(self):
        out = ""
        for i, manipulation in enumerate(self.manipulations):
                out+= "\n{} -- {}".format(i+1, manipulation.get_operation_name())
        return out
    



# df = pd.read_csv("Sample_Data/excited_tracks_truncated.csv", index_col=0)
# proc = preprocessor(df)
# m1 = manipulator(drop_columns, ["release_date"])
# m2 = manipulator(drop_rows, [0,1])
# proc.append_manipulation(m1)
# proc.append_manipulation(m2)
# print(proc.get_manipulation_names())
# print(df.shape)
# df_new = proc.preprocess()
# print(df_new.shape)
        
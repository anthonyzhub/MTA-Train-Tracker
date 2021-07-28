import pandas as pd

class StationsData:

    def __init__(self) -> None:
        
        # Import CSV file as a pandas' dataframe
        self.df = pd.read_csv("stations.csv")
        
        # Create a dictionary to save station's name with ID
        self.stationNamesDict = dict()

    def printDictionary(self):

        for k, v in self.stationNamesDict.items():
            print(k, v)

    def stationIDToName(self):

        # OBJECTIVE: Automatically store station's name with ID

        # Iterate dataframe
        for row in self.df.itertuples():

            # Save station's name as key and station's ID as value
            self.stationNamesDict[row[3]] = row[1]

        # self.printDictionary()
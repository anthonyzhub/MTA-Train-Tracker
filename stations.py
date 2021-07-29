import pandas as pd

class StationsData:

    def __init__(self) -> None:
        
        # Import CSV file as a pandas' dataframe
        self.df = pd.read_csv("Stations - Preferred Trains.csv")

        # Create a list of stations to watchout for
        self.preferredStationsList = ["ADD YOUR STATION'S NAME HERE. MAKE SURE IT IS WRITTEN EXACTLY BY THE MTA IN THEIR EXCEL SHEET."]
        self.savedStationsDict = dict()

    def printDictionary(self, currDict):

        for k, v in currDict.items():
            print(k, v)

    def saveStationToDict(self):

        # OBJECTIVE: Go through CSV file and get station's ID, name, and daytime routine

        def getStationsBefore(stop_id):

            # OBJECTIVE: Create a list of 5 train stations' id before "stop_id"

            # Save letter from "stop_id"
            # NOTE: Some stations have a letter before the station's id number
            stationLetter = str()
            if not stop_id.isnumeric():
                stationLetter = stop_id[0]
                stop_id = stop_id[1:]

            # Create a list of stations' ID
            stationsBefore = list()

            # Iterate range
            # NOTE: Creating 5 IDs for 5 stations before "stop_id"
            stop_id = int(stop_id)
            for i in range(stop_id - 5, stop_id + 1):

                # NOTE: MTA doesn't have any stations with IDs less than or equal to 0
                if i > 0:

                    # If "stop_id" never started with a letter, add it independently to list.
                    # If not, then string might need to be padded before adding it to list
                    # E.g. "Q04" is a valid station id, then "Q4"
                    if stationLetter == "":
                        stationsBefore.append(str(i))
                    else:

                        # If "i" is a single digit digit, then pad string with a 0
                        # If not, add "stationLetter" and "i" together to list
                        if i < 10:
                            stationsBefore.append(stationLetter + "0" + str(i))
                        else:
                            stationsBefore.append(stationLetter + str(i))
            
            return stationsBefore

        # Iterate imported dataframe
        for row in self.df.itertuples():
            # print(row)
            # If row has a station name that is inside class' list, then add it to dictionary
            if row[3] in self.preferredStationsList:

                # Extract stop_id, daytime route, and 5 stops north of preferred station
                stop_id = row[1]
                lineName = row[2]
                trainsStoppingList = list(row[4].replace(" ", ""))
                stationsBeforeList = getStationsBefore(stop_id)
                
                # If a route is labeled in thousands, replace it with last digit
                # NOTE: If a station accepts local and express trains, local trains are expressed in thousands
                # E.g. A 6 train in Grand Central station is orginally labeled as "2006" in CSV, so route ID will be renamed to "6."
                if len(trainsStoppingList[-1]) > 1:
                    trainsStoppingList[-1] = trainsStoppingList[-1][-1]

                # NOTE: {station name: (stop ID, line name, Daytime Route, 5 stops before preferred station)}
                self.savedStationsDict[row[3]] = (stop_id, lineName, trainsStoppingList, stationsBeforeList)

        # self.printDictionary(self.savedStationsDict)
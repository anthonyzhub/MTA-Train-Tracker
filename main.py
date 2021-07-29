#! /usr/bin/python3
from access import Access
from stations import StationsData
from manage import ManageData

def main():

    # Load CSV as pandas' data frame
    stationsClass = StationsData()
    stationsClass.saveStationToDict()

    # Initialize class before connecting to MTA
    accessClass = Access()
    accessClass.getData()

    # Manipulate Data
    managementClass = ManageData(accessClass.protocolBufferDataList, stationsClass.savedStationsDict)

    # Print a train's ETA for each station
    for station in stationsClass.preferredStationsList:
        managementClass.setPreferredStation(station)
        managementClass.calculateTrainsETAToStation()
        print()

if __name__ == "__main__":

    main()
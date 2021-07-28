#! /usr/bin/python3
from access import Access
from stations import StationsData
from manage import ManageData

if __name__ == "__main__":

    # Load CSV as pandas' data frame
    stationsClass = StationsData()
    stationsClass.stationIDToName()

    # Connect to MTA
    accessClass = Access()
    accessClass.getData()

    # Initialize class to manipulate data
    managementClass = ManageData(accessClass.raw_proto_buff_data, stationsClass.stationNamesDict)

    upcomingTrainToHuntsPoint = managementClass.getTrainsBeforeDesignatedStop("Hunts Point Av")
    managementClass.calculateTrainsETAToStation(upcomingTrainToHuntsPoint, "Hunts Point Av")

    upcomingTrainToSimpsonSt = managementClass.getTrainsBeforeDesignatedStop("Simpson St")
    managementClass.calculateTrainsETAToStation(upcomingTrainToSimpsonSt, "Simpson St")

    managementClass.printETADictionary()
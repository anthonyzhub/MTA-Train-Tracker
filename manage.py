from protobuf_to_dict import protobuf_to_dict
import time

class ManageData:

    def __init__(self, protocol_buffer_data, stationNamesDict) -> None:

        # Convert protocol buffer into a dictionary
        self.dataDictionary = protobuf_to_dict(protocol_buffer_data)
        self.protocol_buffer_data = protocol_buffer_data

        # Save train stops before Hunts Point Av.
        self.stopsBeforeHuntsPointList = [str(i) for i in range(601, 614)] # 613 is Hunts Point
        self.stopsBeforeSimpsonStList = [str(i) for i in range(204, 218)] # 217 is Simpson St.

        # Create a dictionary to save station's id
        self.stationNamesDict = stationNamesDict

        # Create a dictionary to save trains' ETA
        self.trainsETADict = dict()

    def errorMessage(self, message):
        print(message)
        exit(0)

    def printETADictionary(self):

        for key, val in self.trainsETADict.items():
            # print(key, val, "min")
            print("{} arriving in {} minutes".format(key, val))

    def getTripUpdate(self):

        # OBJECTIVE: Iterate data and only get trains

        trainsList = list()

        # Iterate data and only get entity (train)
        for entity in self.protocol_buffer_data.entity:

            # Filter data out by only looking for trains
            try:
                if entity.HasField("trip_update"):
                    trainsList.append(entity)
            except:
                self.errorMessage("'trip_update' does not exist!")

        return trainsList

    def getNumericTrains(self):

        # OBJECTIVE: Get train-only data and only keep data of 2, 5, and 6 trains

        # Get list of entities
        entitiesList = self.getTripUpdate()

        # Create a list to save entities of 2/5/6 trains
        preferedTrains = list()

        # Iterate data and only keep 2/5/6 trains
        for entity in entitiesList:

            # If "route_id" is either a 2/5/6, then keep it
            try:
                if entity.trip_update.HasField("trip"):
                    if entity.trip_update.trip.route_id in ["2", "5", "6"]:
                        # print("{} is a 2/5/6 train".format(entity.id))
                        preferedTrains.append(entity)
            except:
                self.errorMessage("'trip' field does not exist!")

        return preferedTrains

    def getSouthBoundTrains(self):

        # OBJECTIVE: Get train-only data and only keep trains heading downtown

        # Get list of entities
        entitiesList = self.getNumericTrains()
        
        # Create a list to save southbound 2/5/6 trains
        southboundTrains = list()

        # Iterate list and only keep trains heading downtown
        for entity in entitiesList:

            # Check if train is heading downtown based on "stop_id"
            # NOTE: If "stop_id" ends with a "S" for south, then train is heading downtown
            try:
                if entity.trip_update.stop_time_update[0].stop_id[-1] == "S":
                    # print("{} is heading South".format(entity.id))
                    southboundTrains.append(entity)
            except AttributeError as error:
                self.errorMessage("An attribute doesn't exist!\nError: {}".format(error))

        return southboundTrains

    def getTrainsBeforeDesignatedStop(self, preferedStation):

        # OBJECTIVE: Get a list of southbound trains heading to Hunts Point or Simpson street station

        # Create reference to pre-defined lists
        if preferedStation == "Hunts Point Av":
            print("getTrainsBeforeDesignatedStop() => Focusing on Hunts Point Avenue station")
            stopsBeforeDesignatedStation = self.stopsBeforeHuntsPointList
        else:
            print("getTrainsBeforeDesignatedStop() => Focusing on Simpson St. station")
            stopsBeforeDesignatedStation = self.stopsBeforeSimpsonStList

        # Get list of entities
        entitiesList = self.getSouthBoundTrains()

        # Create a list of trains heading to Hunts Point
        upcomingTrains = list()
        
        # Sort list based on "stop_id" value in descending order
        entitiesList.sort(key=lambda entity: entity.trip_update.stop_time_update[0].stop_id, reverse=True)
        
        # Remove trains that already passed Hunts Point Avenue
        for entity in entitiesList:

            # If next stop is not inside the list, then the train has already passed Hunts Point station
            # NOTE: Excluded last character because it indicates direction (north or south)
            if entity.trip_update.stop_time_update[0].stop_id[:-1] in stopsBeforeDesignatedStation:
                # print(entity.trip_update.stop_time_update[0].stop_id)
                upcomingTrains.append(entity)
        
        return upcomingTrains

    def calculateTrainsETAToStation(self, preferredTrainsList, preferredStation):

        # Get station's id
        stop_id = self.stationNamesDict[preferredStation]
        print("calculateTrainsETAToStation() => Calculating ETA to ", preferredStation)

        # Iterate list
        for entity in preferredTrainsList:

            # Create holder variables for future use
            firstStopRecorded = False
            currStopHolder = 0

            # Iterate train's "stop_time_update" until preferred station is found
            for station in range(len(entity.trip_update.stop_time_update)):

                # Create variable to hold reference of station
                currStation = entity.trip_update.stop_time_update[station]
                
                # Record departure time of train's current or incoming stop
                if firstStopRecorded is False:
                    currStopHolder = currStation.departure.time
                    firstStopRecorded = True

                # Get train's arrival time for preferred station
                if currStation.stop_id[:-1] == stop_id:

                    # Save train's ETA to preferred station
                    # NOTE: Subtracting POSIX time which is in seconds
                    tmpKey = entity.id + " - " + entity.trip_update.trip.route_id + " Train"
                    self.trainsETADict[tmpKey] = (currStation.arrival.time - currStopHolder) // 60

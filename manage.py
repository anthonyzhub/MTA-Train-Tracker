class ManageData:

    def __init__(self, protocolBufferDataList, savedStationsDict) -> None:

        # Create a list to save all data received from MTA
        self.protocolBufferDataList = protocolBufferDataList

        # Create a list to save trains to lookout for
        self.preferredTrains = list("2456Q")
        self.savedStationsDict = savedStationsDict

        # Set variable to save preferred station
        self.preferredStation = str()

    def errorMessage(self, message):
        print(message)
        exit(0)

    def setPreferredStation(self, preferredStation):

        # OBJECTIVE: Frequently used function to update string variable
        self.preferredStation = preferredStation

    def getTrainsData(self):

        # OBJECTIVE: Go through GTFS data and only keep data related to trains

        trainsList = list()

        # Iterate data and only get entity (train)
        for elem in self.protocolBufferDataList:
            for entity in elem.entity:

                # Filter data out by only looking for trains
                try:
                    if entity.HasField("trip_update"):
                        trainsList.append(entity)
                except:
                    self.errorMessage("'trip_update' does not exist!")

        return trainsList

    def getSpecificTrains(self):

        # OBJECTIVE: Filter trains-only data to trains that user only cares about

        # Get list of entities
        entitiesList = self.getTrainsData()

        # Create a list to save entities of preferred trains
        preferredTrains = list()

        # Iterate data and only keep preferred trains
        for entity in entitiesList:

            # If "route_id" is saved in list, then keep it
            try:
                if entity.trip_update.HasField("trip"):
                    if entity.trip_update.trip.route_id in self.preferredTrains:
                        # print("{} is a {} train".format(entity.id, entity.trip_update.trip.route_id))
                        preferredTrains.append(entity)
            except:
                self.errorMessage("'trip' field does not exist!")

        return preferredTrains

    def getSouthBoundTrains(self):

        # OBJECTIVE: Get train-only data and only keep trains heading downtown

        # Get list of entities
        entitiesList = self.getSpecificTrains()
        
        # Create a list to save southbound trains
        southboundTrains = list()

        # Iterate list and only keep trains heading downtown
        for entity in entitiesList:

            # Check if train is heading downtown based on "stop_id"
            # NOTE: If "stop_id" ends with a "S" for south, then train is heading downtown
            try:
                
                try:
                    # print(entity.trip_update.stop_time_update[0].stop_id)
                    if entity.trip_update.stop_time_update[0].stop_id[-1] == "S":
                        # print("{} is heading South".format(entity.id))
                        southboundTrains.append(entity)
                except IndexError as error:
                        print(entity.trip_update.stop_time_update)
                        # print(entity.trip_update.stop_time_update[0].stop_id)
                        self.errorMessage("Error might be coming from 'stop_time_update[0]'\n".format(error))

            except AttributeError as error:
                self.errorMessage("An attribute doesn't exist!\nError: {}".format(error))

        return southboundTrains

    def getTrainsBeforeDesignatedStop(self):

        # OBJECTIVE: Get a list of southbound trains heading to Hunts Point or Simpson street station

        # Get list of entities
        entitiesList = self.getSouthBoundTrains()

        # Create a list of trains heading to preferredStation
        upcomingTrains = list()
        
        # Sort list based on "stop_id" value in descending order
        entitiesList.sort(key=lambda entity: entity.trip_update.stop_time_update[0].stop_id, reverse=True)
        
        # Remove trains that already passed preferredStation
        for entity in entitiesList:

            # If next stop is not inside the list, then the train has already passed preferredStation
            # NOTE: Excluded last character because it indicates direction (north or south)
            if entity.trip_update.stop_time_update[0].stop_id[:-1] in self.savedStationsDict[self.preferredStation][3]:
                # print("{} is at {} before {}".format(entity.id, entity.trip_update.stop_time_update[0].stop_id, self.savedStationsDict[self.preferredStation][0]))
                upcomingTrains.append(entity)
        
        return upcomingTrains

    def calculateTrainsETAToStation(self):

        # Get preferredStation's stop_id
        stop_id = self.savedStationsDict[self.preferredStation][0]
        print("calculateTrainsETAToStation() => Calculating ETA to", self.preferredStation)

        # Get a list of southbound trains heading to preferredStation
        availableTrainsList = self.getTrainsBeforeDesignatedStop()

        # Iterate list
        for entity in availableTrainsList:

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
                    tmpETA = (currStation.arrival.time - currStopHolder) // 60

                    if tmpETA <= 1:
                        print("{} train is at the station".format(entity.trip_update.trip.route_id))
                    else:
                        print("{} train arriving in {} minutes".format(entity.trip_update.trip.route_id, tmpETA))

                else:
                    # print("Unable to find {} in train's route".format(stop_id))
                    pass
from google.transit import gtfs_realtime_pb2
import requests
import urllib
import http

class Access:

    def __init__(self) -> None:

        # Define URL for specific train
        #self.g_train_api = ""
        self.numeric_trains_api = "PASTE MTA'S API URL HERE (DEPENDING ON TRAIN)"

        # Define URL header
        self.header = {"x-api-key": "PASTE YOUR PRIVATE API KEY HERE"}

        # Save data across class
        self.raw_proto_buff_data = None
        self.raw_dict_data = dict()

        # Save train stops before Hunts Point Av.
        self.stopsBeforeHuntsPointList = [str(i) for i in range(601, 614)]
        self.stopsBeforeSimpsonStList = [str(i) for i in range(204, 218)]

    def errorMessage(self, message):
        print(message)
        exit(0)

    def getData(self):

        # Perform GET request and wait for a response
        try:
            urlRequest = urllib.request.Request(self.numeric_trains_api, headers=self.header)
            urlResponse = urllib.request.urlopen(urlRequest)
        except urllib.error.HTTPError as error:
            print("Access.connect() Message: Unable to connect to MTA")
            self.errorMessage("HTTP error code is '{}' meaning '{}'".format(error.code, http.HTTPStatus(error.code).phrase))

        # Initialize GTFS object and parse response
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(urlResponse.read())

        # Save data to class variable for future use
        self.raw_proto_buff_data = feed
    """
    def getTripUpdate(self):

        # OBJECTIVE: Iterate data and only get trains

        trainsList = list()

        # Iterate data and only get entity (train)
        for entity in self.raw_proto_buff_data.entity:

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
        
        # Create a list to save soutbound 2/5/6 trains
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

    def getTrainsBeforeHuntsPoint(self):

        # OBJECTIVE: Get a list of southbound trains heading to Hunts Point station

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
            if int(entity.trip_update.stop_time_update[0].stop_id[:-1]) in self.stopsBeforeHuntsPointList:
                upcomingTrains.append(entity)

        return upcomingTrains

    def getTrainsBeforeDesignatedStop(self, preferedStation):

        # OBJECTIVE: Get a list of southbound trains heading to Hunts Point or Simpson street station

        # Create reference to pre-defined lists
        if preferedStation == "Hunts Point":
            print("Focusing on Hunts Point Avenue station")
            stopsBeforeDesignatedStation = self.stopsBeforeHuntsPointList
        else:
            print("Focusing on Simpson St. station")
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
    """
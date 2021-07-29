from google.transit import gtfs_realtime_pb2
import requests
import urllib
import http

class Access:

    def __init__(self) -> None:

        # Define URL for specific train
        self.trainsAPIDict = {
            "Number Train API": "PASTE API HERE",
            "Q Train API": "PASTE API HERE",
        }

        # Define URL header
        self.header = {"x-api-key": "PASTE KEY HERE"}

        # Save data across class
        self.protocolBufferDataList = list()

    def errorMessage(self, message):
        print(message)
        exit(0)

    def getData(self):

        for apiLink in self.trainsAPIDict.values():

            # Perform GET request and wait for a response
            try:
                urlRequest = urllib.request.Request(apiLink, headers=self.header)
                urlResponse = urllib.request.urlopen(urlRequest)
            except urllib.error.HTTPError as error:
                print("Access.connect() Message: Unable to connect to MTA")
                self.errorMessage("HTTP error code is '{}' meaning '{}'".format(error.code, http.HTTPStatus(error.code).phrase))

            # Initialize GTFS object and parse response
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(urlResponse.read())

            # Save data to class variable for future use
            self.protocolBufferDataList.append(feed)

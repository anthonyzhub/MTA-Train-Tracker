# MTA-Train-Tracker
A Python program that extracts data from New York City's MTA using a public API and interacting with Google's Protocol Buffer. The main goal is to predict a train's ETA to a particular station.

# General notes for beginners
- "stop_id" is an identifier for a station
- "stop_id" is created with the 1st letter being a train that stops, the station's number, and which direction the train is going
    E.g. "G30N" translates to G train in station #30 heading north
- The arrival and departure time is in Epoch/POSIX format. 
    I.e. Time passed since January 1, 1970
- Accept terms & condition to get all available data from MTA (http://web.mta.info/developers/developer-data-terms.html#data)

# Libraries needed
1. GTFS Realtime Bindings.
2. Pandas

Execute command: `pip install --upgrade gtfs-realtime-bindings pandas`

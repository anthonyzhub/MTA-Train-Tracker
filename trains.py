import pandas as pd

class Trains:

    def __init__(self, entitiesList) -> None:
        
        self.df = pd.json_normalize(entitiesList)
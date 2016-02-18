__author__ = 'William Johnson'
import json


class CreateJSON:

    def __init__(self, aptInfo):
        self.summary = aptInfo

    # write both json objects to file
    def create(self):
        f = open("aptAPI.json", "w")
        f.write(json.dumps(self.summary, indent=4))
        f.close()

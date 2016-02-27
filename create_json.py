__author__ = 'William Johnson'
import json


class CreateJSON:

    def __init__(self, apt_info):
        self.summary = apt_info

    # write both json objects to file
    def create_org(self):
        f = open("apt_original.json", "w")
        f.write(json.dumps(self.summary, indent=4))
        f.close()

    def create_latest(self):
        f = open("apt_latest.json", "w")
        f.write(json.dumps(self.summary, indent=4))
        f.close()

if __name__ == "main":
    test = CreateJSON()
    #test.create_org()
    test.create_latest()
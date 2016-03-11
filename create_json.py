import json
import os

class CreateJSON:
    def __init__(self, apt_info):
        self.summary = apt_info
        self.file_loc = os.path.dirname(os.path.abspath(__file__))

    # write both json objects to file
    def create_org(self):
        f = open(self.file_loc + '/apt_original.json', 'w')
        f.write(json.dumps(self.summary, indent=4))
        f.close()

    def create_latest(self):
        f = open(self.file_loc + '/apt_latest.json', 'w')
        f.write(json.dumps(self.summary, indent=4))
        f.close()

if __name__ == '__main__':
    test = CreateJSON()
    #test.create_org()
    test.create_latest()

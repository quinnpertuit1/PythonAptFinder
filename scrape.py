import urllib.request
import urllib.parse
import json
from create_json import CreateJSON
import time

class ScrapeAPI:
    def __init__(self):
        # create empty dictionary for apartment info
        self.aptList = []
        self.scrape()

    def scrape(self):
        # url of api
        url = "https://api.avalonbay.com/json/reply/ApartmentSearch"
        # create empty dictionary for API parameters
        query = {}
        # create empty dictionary for apartment summary
        aptInfo = {}
        # create empty list to contain aptList and aptInfo
        aptSummary = []
        # initialize total variable
        total = 0
        # add key & values to dictionary
        query['communityCode'] = 'CA564'
        query['desiredMoveInDate'] = '2016-02-18T07:00:00.000Z'
        query['min'] = '1700'
        query['max'] = '2440'
        # convert dictionary above into url-encoded string
        url_values = urllib.parse.urlencode(query)
        # append url_values to url from line 6
        full_url = url + '?' + url_values
        print(full_url)
        # Generate HTTP GET Request with full_url variable from above
        api = urllib.request.Request(url=full_url, method='GET')
        with urllib.request.urlopen(api) as response:
            # decode from bytes (Unicode) to string
            data = response.read().decode('utf-8')
            parsed_json = json.loads(data)
            # Finds how many types are in AvailableFloorPlanTypes array
            elements = len(parsed_json['results']['availableFloorPlanTypes'])
            for i in range(elements):
                # Number of floor plans in availableFloorPlans array
                numOfFloorPlans = len(parsed_json['results']['availableFloorPlanTypes'][i]['availableFloorPlans'])
                # Array of available floor plans and apartments (
                floorPlan = parsed_json['results']['availableFloorPlanTypes'][i]['availableFloorPlans']
                # Type of floor plan (Studio, 1 bed)
                aptRooms = parsed_json['results']['availableFloorPlanTypes'][i]['display']
                print(str(numOfFloorPlans) + " floor plans available for " + aptRooms + " apartments")
                for index in range(numOfFloorPlans):
                    # Length of apartments array inside of finishPackages array
                    total += len(floorPlan[index]['finishPackages'][0]['apartments'])
                    for index2 in range(len(floorPlan[index]['finishPackages'][0]['apartments'])):
                        # Shorten length of index required to access value
                        short_apt = floorPlan[index]['finishPackages'][0]['apartments'][index2]
                        date = time.strftime('%Y-%m-%d', time.gmtime(int(short_apt['pricing']['availableDate'][6:19])/1000))
                        apts = {
                            'aptNum': short_apt['apartmentNumber'],
                            'aptSize': short_apt['apartmentSize'],
                            'aptPrice': short_apt['pricing']['effectiveRent'],
                            'aptAvailDate': date
                        }
                        self.aptList.append(apts)
                print(str(total) + "  apartments available")

                # add variables to floor plan summary dictionary for JSON
                floorPlanSummary = {
                    'name': aptRooms,
                    'floor_plans': numOfFloorPlans,
                    'total': str(total)
                }
                # re-assign total to zero for next iteration
                total = 0
                aptSummary.append(floorPlanSummary)
            aptInfo['summary'] = aptSummary
            aptInfo['apartments'] = self.aptList
            test = CreateJSON(aptInfo)
            test.create()

    def get_data(self):
        return self.aptList

    def main(self):
        self.scrape()
        self.get_data()

if __name__ == "__main__":
    test = ScrapeAPI()
    test.get_data()

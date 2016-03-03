import urllib.request
import urllib.parse
import json
from create_json import CreateJSON
import time


class ScrapeAPI:
    def __init__(self, rent_min, rent_max, rent_date, search_type):
        # create empty dictionary for apartment info
        self.aptList = []
        self.rent_min = rent_min
        self.rent_max = rent_max
        self.rent_date = rent_date
        self.search_type = search_type

    def scrape(self):
        # url of api
        url = "https://api.avalonbay.com/json/reply/ApartmentSearch"
        # create empty dictionary for API parameters
        query = {}
        # create empty dictionary for apartment summary
        apt_info = {}
        # create empty list to contain aptList and aptInfo
        apt_summary = []
        # initialize total variable
        total = 0
        # add key & values to dictionary
        query['communityCode'] = 'CA564'
        query['desiredMoveInDate'] = self.rent_date + 'T08:00:00.000Z'
        query['min'] = self.rent_min
        query['max'] = self.rent_max
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
                num_of_floor_plans = len(parsed_json['results']['availableFloorPlanTypes'][i]['availableFloorPlans'])
                # Array of available floor plans and apartments (
                floor_plan = parsed_json['results']['availableFloorPlanTypes'][i]['availableFloorPlans']
                # Type of floor plan (Studio, 1 bed)
                apt_rooms = parsed_json['results']['availableFloorPlanTypes'][i]['display']
                print(str(num_of_floor_plans) + " floor plans available for " + apt_rooms + " apartments")
                for index in range(num_of_floor_plans):
                    # Length of apartments array inside of finishPackages array
                    total += len(floor_plan[index]['finishPackages'][0]['apartments'])
                    for index2 in range(len(floor_plan[index]['finishPackages'][0]['apartments'])):
                        # Shorten length of index required to access value
                        short_apt = floor_plan[index]['finishPackages'][0]['apartments'][index2]
                        rent_date = time.strftime('%Y-%m-%d', time.gmtime(int(short_apt['pricing']['availableDate'][6:19]) / 1000))
                        apts = {
                            'aptNum': short_apt['apartmentNumber'],
                            'aptSize': short_apt['apartmentSize'],
                            'aptPrice': short_apt['pricing']['effectiveRent'],
                            'aptAvailDate': rent_date
                        }
                        self.aptList.append(apts)
                print(str(total) + "  apartments available")

                # add variables to floor plan summary dictionary for JSON
                floor_plan_summary = {
                    'name': apt_rooms,
                    'floor_plans': num_of_floor_plans,
                    'total': str(total)
                }
                # re-assign total to zero for next iteration
                total = 0
                apt_summary.append(floor_plan_summary)
            apt_info['summary'] = apt_summary
            apt_info['apartments'] = self.aptList
            apt_json = CreateJSON(apt_info)
            # Determine which json file to create
            if self.search_type == 'org':
                apt_json.create_org()
            else:
                apt_json.create_latest()

    # return apartment data
    def get_data(self):
        return self.aptList

if __name__ == "__main__":
    search = ScrapeAPI(2000, 3000, '2016-02-26', 'org')
    search.scrape()

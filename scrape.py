import urllib.request
import urllib.parse
import json
from create_json import CreateJSON
import time
import sys


# create empty dictionary for apartment info
print(sys.argv[3])
aptList = []
rent_min = sys.argv[1]
rent_max = sys.argv[2]
rent_date = sys.argv[3]
search_type = sys.argv[4]
print(type(sys.argv[1]))

def scrape():
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
    query['desiredMoveInDate'] = rent_date + 'T07:00:00.000Z'
    print(query['desiredMoveInDate'])
    query['min'] = rent_min
    query['max'] = rent_max
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
                    avail_date = time.strftime('%Y-%m-%d', time.gmtime(int(short_apt['pricing']['availableDate'][6:19]) / 1000))
                    apts = {
                        'aptNum': short_apt['apartmentNumber'],
                        'aptSize': short_apt['apartmentSize'],
                        'aptPrice': short_apt['pricing']['effectiveRent'],
                        'aptAvailDate': avail_date
                    }
                    aptList.append(apts)
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
            apt_info['apartments'] = aptList
            apt_json = CreateJSON(apt_info)
            # Determine which json file to create
        print(type(search_type))
        if search_type == 'org':
            apt_json.create_org()
        else:
            print(search_type)
            apt_json.create_latest()

if __name__ == "__main__":
    scrape()

import urllib.request
import urllib.parse
import json

# url of api
url = "https://api.avalonbay.com/json/reply/ApartmentSearch"
# create empty dictionary
query = {}
# intialize total variable
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
api = urllib.request.Request(url=full_url, method='GET')
with urllib.request.urlopen(api) as response:
    # decode from bytes (Unicode) to string
    data = response.read().decode('utf-8')
    parsed_json = json.loads(data)
    # Finds how many elements are in results array
    elements = len(parsed_json['results']['availableFloorPlanTypes'])
    for i in range(elements):
        size = len(parsed_json['results']['availableFloorPlanTypes'][i]['availableFloorPlans'])
        shorten = parsed_json['results']['availableFloorPlanTypes'][i]['availableFloorPlans']
        print(str(size) + " floor plans available for " + parsed_json['results']['availableFloorPlanTypes'][i]['display'] + " apartments")
        for index in range(size):
            total += len(shorten[index]['finishPackages'][0]['apartments'])
        print(str(total)+ "  apartments available")
        total = 0
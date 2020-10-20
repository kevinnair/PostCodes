import requests
import sys
import re

# https://en.wikipedia.org/wiki/Postcodes_in_the_United_Kingdom
# https://en.wikipedia.org/wiki/Postcodes_in_the_United_Kingdom#Special_cases

postcode = None
while True:
    try:
        standard_input = input("Enter Postcode:")
        match = re.search(r"^(([A-Z]{1,2}[0-9][A-Z0-9]?|ASCN|STHL|TDCU|BBND|[BFS]IQQ|PCRN|TKCA) ?[0-9][A-Z]{2}|BFPO ?[0-9]{1,4}|(KY[0-9]|MSR|VG|AI)[ -]?[0-9]{4}|[A-Z]{2} ?[0-9]{2}|GE ?CX|GIR ?0A{2}|SAN ?TA1)$", standard_input.upper())
        if match is None:
            print("Sorry that postcode is not valid, please try again.\n")
            continue
        else:
            postcode = match.string.upper()
            break
    except ValueError:
        print("Sorry that postcode is not valid, please try again.\n")
        continue
    

baseurl = "http://postcodes.io"

def getRegionAndCountry(postcode):
    response = requests.get(baseurl + "/postcodes/" + postcode)
    data = response.json()
    for item in data["result"]:
        if item == "country" or item == "region":
            print(item.upper() + ": " +  data["result"][item])


def validate(postcode):
    response = requests.get(baseurl + "/postcodes/" + postcode + "/validate")
    data = response.json()
    return data["result"]

def nearest(postcode):
    response = requests.get(baseurl + "/postcodes/" + postcode + "/nearest", {"radius": 200})
    data = response.json()
    for item in data["result"]:
        longitude = item["longitude"]
        latitude = item["latitude"]    
        res = requests.get(baseurl + "/postcodes?lon=" + str(longitude) + "&lat=" + str(latitude))
        dat = res.json()
        for result in dat["result"]:
            for subitem in result:
                if subitem == "postcode" or subitem == "region" or subitem == "country":
                    print(subitem.upper() + ": " + result[subitem])
            print("\n")

try:
    valid = validate(postcode)
    if(valid is False):
        print("Sorry that postcode is not valid, please try again.\n")
        sys.exit(0)
    print("\n\nQuerying...\nPOSTCODE: " + postcode)
    getRegionAndCountry(postcode)
    print("\nNearby postcodes (inclusive):\n")
    nearest(postcode)
except requests.exceptions.RequestException as e:
    print("Sorry that postcode is not valid, please try again.\n")
    raise SystemExit(e)
except requests.exceptions.timeout:
    print("Sorry, the server did not respond in time. Please try again.\n")
    sys.exit(0)
except:
    print("Sorry, something went wrong. Please try again later.\n")
    sys.exit(0)
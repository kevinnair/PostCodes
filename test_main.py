import re
import requests

## Main file input testing
def validateInputRegex(postcode):
    match = re.search(r"^(([A-Z]{1,2}[0-9][A-Z0-9]?|ASCN|STHL|TDCU|BBND|[BFS]IQQ|PCRN|TKCA) ?[0-9][A-Z]{2}|BFPO ?[0-9]{1,4}|(KY[0-9]|MSR|VG|AI)[ -]?[0-9]{4}|[A-Z]{2} ?[0-9]{2}|GE ?CX|GIR ?0A{2}|SAN ?TA1)$", postcode)
    return match

def test_validateInputRegex():
    assert validateInputRegex("CB30FA") is not None
    assert validateInputRegex("ASDF") is None
    assert validateInputRegex("") is None
    assert validateInputRegex("      ") is None
    assert validateInputRegex("CB30FF") is not None
    assert validateInputRegex("BS981TL") is not None #special postcodes
    assert validateInputRegex("SA99") is not None

## Basic API Int Testing
baseurl = "http://postcodes.io"
def apiValidate(postcode):
    response = requests.get(baseurl + "/postcodes/" + postcode + "/validate")
    data = response.json()
    return data["result"]

def test_apiValidate():
    assert apiValidate("CB30FA") == True
    assert apiValidate("ASDF") == False
    assert apiValidate("CB30FF") == True
    assert apiValidate("ABC123123") == False

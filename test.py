import time

from user_data import *


while True:
    _jsonFile = open("userData.json", "r")
    _jsonText = _jsonFile.read()
    _jsonFile.close()
    _convertedDict = json.loads(_jsonText)
    print(_convertedDict["Ads"])
#dictionary import

from datetime import timedelta
tunnelLength = 2690
totalTunnelZone = tunnelLength

dataDict = {}
carSpeeds = {}
speeding = []
safe = []

fileName = "tunnel times fuller set.csv"

fileData = open(fileName, "r")
dataLines = fileData.readlines()
for data in dataLines:
    #print(data)
    dataKey, dataValue = data.split(",")
    dataValue = ((dataValue.split("\n"))[0])
    if dataKey not in dataDict.keys():
        dataDict.setdefault(dataKey, [])
        dataDict[dataKey].append(dataValue)
    else:
        dataDict[dataKey].append(dataValue)

for data in dataDict.keys():
    entryTime = ((dataDict[data])[0])
    exitTime = ((dataDict[data])[1])
    print(entryTime, exitTime)
    entryTimeSplit = entryTime.split(":")
    exitTimeSplit = exitTime.split(":")
    entryTimeInSec = timedelta(hours=int((entryTimeSplit[0])), minutes=int((entryTimeSplit[1])), seconds=int((entryTimeSplit[2])))
    exitTimeInSec = timedelta(hours=int((exitTimeSplit[0])), minutes=int((exitTimeSplit[1])), seconds=int((exitTimeSplit[2])))
    differenceInTime = (exitTimeInSec.total_seconds() - entryTimeInSec.total_seconds())
    metersPerSecond = totalTunnelZone / differenceInTime
    kmPerHour = (metersPerSecond * 3600) / 1000
    print("{}".format(kmPerHour))
    carSpeeds[data] = kmPerHour
    if kmPerHour > 85:
        speeding.append(data)
    else:
        safe.append(data)
print("SPEEEEEEEEEEEEEEEEEEEED")
print(len(speeding))
for key in speeding:
    print(key, dataDict[key])
print("+++++++++++++++++++++++")
print("SAFEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
print("SPEEEEEEEEEEEEEEEEEEEED")
print(len(safe))
for key in safe:
    print(key, dataDict[key])
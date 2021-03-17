#Simple Dictionary import
import time
from datetime import timedelta

speedDataName = "test_tunnel.txt"
speedFinesName = "fine_rates.txt"

tunnelLength = 2690
speedLimit = 80
totalTunnelZone = tunnelLength


dataDict = {}
carSpeeds = {}
speeding = []
safe = []
speedFines = []

speedFileData = open(speedDataName, "r")
speedFinesData = open(speedFinesName, "r")


finesLines = speedFinesData.readlines()
for fines in finesLines:
    tempFineAndFee = []
    fineAndFee = fines.split('-')
    fine = fineAndFee[2]
    fineAndFee.remove(fineAndFee[2])
    fine = fine.split("\n")
    fineAndFee.append(fine[0])
    for item in fineAndFee:
        item = int(item)
        tempFineAndFee.append(item)
    speedFines.append(tempFineAndFee)
    #print(speedFines)
dataLines = speedFileData.readlines()
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
    #print(entryTime, exitTime)
    entryTimeSplit = entryTime.split(":")
    exitTimeSplit = exitTime.split(":")
    entryTimeInSec = timedelta(hours=int((entryTimeSplit[0])), minutes=int((entryTimeSplit[1])), seconds=int((entryTimeSplit[2])))
    exitTimeInSec = timedelta(hours=int((exitTimeSplit[0])), minutes=int((exitTimeSplit[1])), seconds=int((exitTimeSplit[2])))
    differenceInTime = (exitTimeInSec.total_seconds() - entryTimeInSec.total_seconds())
    metersPerSecond = totalTunnelZone / differenceInTime
    kmPerHour = (metersPerSecond * 3600) / 1000
    kmPerHour = int(kmPerHour)
    #print("{}".format(kmPerHour))
    carSpeeds[data] = kmPerHour
    #print(data, ",", round(kmPerHour, 2))

#print(speedFines)

maxSpeed = ((speedFines[-1])[1])
maxFine = ((speedFines[-1])[2])



for carPlate in carSpeeds.keys():
    #print(carPlate,",", carSpeeds[carPlate])
    for speedRange in speedFines:
        speed = (carSpeeds[carPlate] - speedLimit)
        speedRangeMin = speedRange[0]
        speedRangeMax = speedRange[1]
        if (speed <= speedRangeMax) and (speed >= speedRangeMin):
            carFine = speedRange[2]
            print("{} speed is {} so fine is {}".format(carPlate, carSpeeds[carPlate], carFine))
            continue
    if speed > maxSpeed:
        print("{} speed is {} so fine is {}".format(carPlate, carSpeeds[carPlate], maxFine))

time.sleep(50)

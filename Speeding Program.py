#Simple Dictionary import

from datetime import timedelta
tunnelLength = 2690
totalTunnelZone = tunnelLength
speedLimit = 80

dataDict = {}
carSpeeds = {}
speeding = []
safe = []
speedFines = []

speedDataName = "tunnel times fuller set.csv"
speedFinesName = "fine_rates.txt"

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
        speed = (carSpeeds[carPlate] - 80)
        speedRangeMin = speedRange[0]
        speedRangeMax = speedRange[1]
        if (speed <= speedRangeMax) and (speed >= speedRangeMin):
            carFine = speedRange[2]
            print("{} speed is {} so fine is {}".format(carPlate, carSpeeds[carPlate], carFine))
            continue
        if speed > maxSpeed:
            print("{} speed is {} so fine is {}".format(carPlate, carSpeeds[carPlate], maxFine))
        
        
#print(speedFines)
#for i in carPlate:
    #print(i)
#print(speedFines)

#for key in carPlate:
    #print(key,",", dataDict[key])

#print("====================")
#for key in safe:
    #print(key,",", dataDict[key])

'''
for speedRange in speedFines:
    #print(speedRange)
    for dataKey in carPlate:
        #print(dataKey)
        carSpeed = int(carSpeeds[dataKey])
        #print(speedRange[1], carSpeed , speedRange[0])
        #if speedRange[1] > (carSpeed - speedLimit) and (carSpeed - speedLimit) > speedRange[0]:
            ##print("TRUE")
            #print("{} speed is {}KM/HR so fine is ${}".format(dataKey, int(carSpeed), speedRange[2]))
        #print("{} speed is {} so fine is {}".format(dataKey, carSpeed, speedRange[2]))
        
        #print("{} speed is {}KM/HR so fine is ${}".format(dataKey, int(carSpeed), 0))
'''
           
'''
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
'''



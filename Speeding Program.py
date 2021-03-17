#Simple Dictionary import
import sys
import time
from datetime import timedelta

#speedDataName = "tunnel times fuller set.csvs"
speedFinesName = "fine_rates.txt"
defaultFinesData = ["1-10-30\n", 
                    "11-15-80\n", 
                    "16-20-120\n", 
                    "21-25-170\n", 
                    "26-30-230\n", 
                    "31-35-300\n", 
                    "36-40-400\n", 
                    "41-45-510\n", 
                    "46-50-630"]

tunnelLength = 2690
speedLimit = 80
totalTunnelZone = tunnelLength


dataDict = {}
carSpeeds = {}
speeding = []
safe = []
speedFines = []


def finesFileCheck():
        try:    
                #print("opening fines file")
                speedFinesData = open(speedFinesName, "r")
                return speedFinesData
        except FileNotFoundError:
                defaultFinesFile = open("fine_rates.txt", "w+")
                for fineRanges in defaultFinesData:
                        defaultFinesFile.write(fineRanges)
                defaultFinesFile.close()
                speedFinesData = open("fine_rates.txt", "r")
                print('WARNING: A FINE RATES TIME DOES NOT EXSIST A DEFAULT "FINE RATES" FILE WILL BE CREATED!!!!')
                time.sleep(2)
                return speedFinesData

def finesFileFormatCheck(speedFinesData):
        errorOccur = False
        lineCounter = 0
        fineLines = speedFinesData.readlines()
        for fines in fineLines:
                try:
                        lineCounter += 1
                        tempFineAndFee = []
                        fineAndFee = fines.split('-')
                        if len(fineAndFee) > 3 or len(fineAndFee) < 3:
                                print("WARNING!: Formatting occured in fine_rates.txt file on line {}: {}".format(lineCounter, fines))
                                errorOccur = True
                                continue
                        fine = fineAndFee[2]
                        fineAndFee.remove(fineAndFee[2])
                        fine = fine.split("\n")
                        fineAndFee.append(fine[0])
                        for item in fineAndFee:
                                item = int(item)
                                tempFineAndFee.append(item)
                        speedFines.append(tempFineAndFee)
                except:
                        if fines != "\n":
                                print("WARNING!: Formatting occured in fine_rates.txt file on line {}: {}".format(lineCounter, fines))
                                time.sleep(1)
                                errorOccur = True
        return speedFines, errorOccur

def speedFileCheck():
        dataDict = {}
        speedFormatError = False
        speedFileLineCounter = 0
        try:    
                speedDataName = input("\nPlease input the name of the data file: ")
                speedFileData = open(speedDataName, "r")
                
                dataLines = speedFileData.readlines()
                for data in dataLines:
                        speedFileLineCounter += 1
                        if data == "\n":
                                continue
                        #print(data)
                        dataKey, dataValue = data.split(",")
                        dataValue = ((dataValue.split("\n"))[0])
                        if dataKey not in dataDict.keys():
                                dataDict.setdefault(dataKey, [])
                                dataDict[dataKey].append(dataValue)
                        else:
                                dataDict[dataKey].append(dataValue)                
                return dataDict, speedFormatError
        except FileNotFoundError:
                print('WARNING!! This data file called "{}" does NOT EXIST!!'.format(speedDataName))
                print("Please check your file name or enter another file name.")
                print("Make sure the file is in the correct directory!")
                speedFileCheck()
        except:
                print("WARNING!!! Error occurred on line {}: {}".format(speedFileLineCounter, data))
                speedFormatError = True
                
def continueOrExitForFines():
        print("Formatting Error occurred on the lines presented above.")
        print("Please Correct the formatting before running this program again.")
        print("You can also choose to delete the 'fine_rates.txt' file and the")
        print("program will automatically create a new one for you.")
        print("The default format is for range of fine rates is: MinSpeed-MaxSpeed-FineAmount\n")
        print("However, you can also choose to continue but the program may not work as intended\n")
        while True:
                try:    
                        print("\nWould you like to continue or exit the program")
                        print("WARNING!: Continuing may not work as intended! ie missing values / calculations")
                        continueState = (input("Type YES to exit or NO to continue the program: ")).lower()
                        if continueState == "yes" or continueState == "y":
                                return True
                        if continueState == "no" or continueState == "n":
                                return False
                        if continueState == "":
                                print("Nothing was entered\n")
                except:
                        print("invalid input")


def speedDataFormatError():
        print("Formatting Error occurred on the lines presented above.")
        print("Please Correct the formatting for the above data before choosing to run this file again.")
        print("The default format is for an speed entry is;  {Registration},HH:MM:SS\n")
        print("However, you can also choose to continue but the program may not work as intended:")
        print("ie. missing entries / miss calculations")
        while True:
                try:    
                        print("\nWould you like to continue or exit the program")
                        print("WARNING!: Continuing may not work as intended! ie entries / calculations")
                        continueState = (input("Type YES to exit or NO to continue the program: ")).lower()
                        if continueState == "yes" or continueState == "y":
                                return True
                        if continueState == "no" or continueState == "n":
                                return False
                        if continueState == "":
                                print("Nothing was entered\n")
                except:
                        print("invalid input") 

def continueOrExitDueToFormat(continueState):
        if continueState is True:
                print("\nExiting Program . . .")
                time.sleep(2)
                sys.exit()
        if continueState is False:
                print("\nContinuing Program: WARNING!: Continuing may not work as intended!\n")
                time.sleep(2)              
speedFinesData = finesFileCheck()
speedFines, formattingErrorForFineRates = finesFileFormatCheck(speedFinesData)
print(speedFines)

if formattingErrorForFineRates is True:
        #include a option to simply create a new fine rates file in program
        continueState = continueOrExitForFines()
        continueOrExitDueToFormat(continueState)

dataDict, speedFormatError = speedFileCheck()
if speedFormatError is True:
        continueState = speedDataFormatError()
        continueOrExitDueToFormat(continueState)

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
        if (speed <= 0 ):
                carFine = None
                print("{} speed is {} so fine is {}".format(carPlate, carSpeeds[carPlate], carFine))
                continue                
        if speed > maxSpeed:
                print("{} speed is {} so fine is {}".format(carPlate, carSpeeds[carPlate], maxFine))

time.sleep(1)

# US - Speeding Program By ZFC

import sys
import time
from datetime import timedelta

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
#warningSpeed = 7 # in km/hr
#warningTimeLimit = int((tunnelLength / ((warningSpeed*1000)/3600))/60)
warningTimeLimit = 30
warningSpeed = int(((tunnelLength / (warningTimeLimit*60))*3.6))
print(warningSpeed)
totalTunnelZone = tunnelLength


dataDict = {}
carSpeeds = {}
speeding = []
safe = []
speedFines = []


def finesFileCheck():
        try:
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
                        if fines == "\n":
                                continue
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
                                print("Except: WARNING!: Formatting occured in fine_rates.txt file on line {}: {}".format(lineCounter, fines))
                                time.sleep(1)
                                errorOccur = True
        return speedFines, errorOccur

def speedFileCheck():
        while True:
                try:
                        speedFileName = input("\nPlease input the name of the data file: ")
                        if speedFileName == "" or speedFileName == " ":
                                print("WARNING!!! : PLEASE DO NOT LEAVE BLANK!!!\n")
                                continue
                        speedFileData = open(speedFileName, "r")
                        speedFileData.close()
                        return speedFileName

                except FileNotFoundError:
                        print('WARNING!! This data file called "{}" does NOT EXIST!!'.format(speedFileName))
                        print("Please check your file name or enter another file name.")
                        print("Make sure the file is in the correct directory!")


def speedFileFormatCheck(speedFileName):
        errorCarData = []
        dataDict = {}
        speedFileName = speedFileName
        speedFormatError = False
        speedFileLineCounter = 0
        while True:
                try:
                        speedFileData = open(speedFileName, "r")

                        dataLines = speedFileData.readlines()
                        for data in dataLines:
                                speedFileLineCounter += 1
                                if data == "\n":
                                        continue
                                dataKey, dataValue = data.split(",")
                                if dataKey in errorCarData:
                                        continue
                                dataValue = ((dataValue.split("\n"))[0])
                                checkValue = dataValue.replace(":", "")
                                if int(checkValue) is False:
                                        print("WARNING!!! Error occurred on line {}: {}".format(speedFileLineCounter, data))
                                        speedFormatError = True
                                        errorCarData.append(dataKey)
                                if dataKey not in dataDict.keys():
                                        dataKey = dataKey
                                        dataDict.setdefault(dataKey, [])
                                        dataDict[dataKey].append(dataValue)
                                else:
                                        dataDict[dataKey].append(dataValue)
                                
                        return dataDict, speedFormatError
                except:
                        print("\nExcept: WARNING!!! Error occurred on line {}: {}".format(speedFileLineCounter, data))
                        speedFormatError = True
                        try:
                                errorCarData.append(dataKey)
                        except:
                                return dataDict, speedFormatError

def continueOrExitForFines():
        print("#=#=#=#=# !!!PLEASE READ!!! #=#=#=#=#\n")
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
                        continueState = (input("Type EXIT to exit or CONTINUE to continue the program: ")).lower()
                        if continueState == "exit" or continueState == "e":
                                return True
                        if continueState == "continue" or continueState == "c":
                                return False
                        if continueState == "" or continueState == " ":
                                print("Nothing was entered\n")
                except:
                        print("invalid input")


def speedDataFormatError():
        print("=========================================================================================")
        print("Formatting Error occurred on the lines presented above.")
        print("Please Correct the formatting for the above data before choosing to run this file again.")
        print("The default format is for an speed entry is;  {Registration},HH:MM:SS\n")
        print("However, you can also choose to continue but the program may not work as intended:")
        print("ie. missing entries / miss calculations")
        while True:
                try:
                        print("\nWould you like to continue or exit the program")
                        print("WARNING!: Continuing may not work as intended! ie entries / calculations")
                        continueState = (input("Type EXIT to exit or CONTINUE to continue the program: ")).lower()
                        if continueState == "exit" or continueState == "e":
                                return True
                        if continueState == "continue" or continueState == "c":
                                return False
                        if continueState == "" or continueState == " ":
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
                

def calculateSpeedPerHr(dataDict):
        for data in dataDict.keys():
                if len(dataDict[data]) < 2:
                        if len(dataDict[data]) == 0:
                                print("WARNING!!! Car with unknown Plate has entered/exited at".format(dataDict[data]))
                                continue
                        print("WARNING!!! Car: {} has not been reported to have exited tunnel!!!".format(data))
                        continue
                
                entryTime = ((dataDict[data])[0])
                exitTime = ((dataDict[data])[1])
                if entryTime == exitTime:
                        print("{} WARNING!!! : ERROR: ENTRY TIME IS THE SAME AS THE EXIT TIME! ".format(data))
                        continue
                entryTimeSplit = entryTime.split(":")
                exitTimeSplit = exitTime.split(":")
                entryTimeInSec = timedelta(hours=int((entryTimeSplit[0])), minutes=int((entryTimeSplit[1])), seconds=int((entryTimeSplit[2])))
                exitTimeInSec = timedelta(hours=int((exitTimeSplit[0])), minutes=int((exitTimeSplit[1])), seconds=int((exitTimeSplit[2])))
                differenceInTime = (exitTimeInSec.total_seconds() - entryTimeInSec.total_seconds())
                metersPerSecond = totalTunnelZone / differenceInTime
                kmPerHour = (metersPerSecond * 3600) / 1000
                kmPerHour = int(kmPerHour)
                carSpeeds[data] = kmPerHour
                
        return carSpeeds

def calculateFines(carSpeeds):
        
        for carPlate in carSpeeds.keys():
                for speedRange in speedFines:
                        speed = (carSpeeds[carPlate] - speedLimit)
                        speedRangeMin = speedRange[0]
                        speedRangeMax = speedRange[1]
                        if (speed <= speedRangeMax) and (speed >= speedRangeMin):
                                carFine = speedRange[2]
                                print("{} speed is {} km/hr so fine is ${}".format(carPlate, carSpeeds[carPlate], carFine))
                                continue
                if (speed + 80) <= warningSpeed:
                        print("WARNING!!! Car: {} has was in the tunnel for more than {} minutes".format(carPlate, warningTimeLimit))  
                if (speed <= 0):
                        carFine = 0
                        print("{} speed is {} km/hr so fine is ${}".format(carPlate, carSpeeds[carPlate], carFine))
                if speed > maxSpeed:
                        print("{} speed is {} km/hr so fine is ${}".format(carPlate, carSpeeds[carPlate], maxFine))
                continue
                

speedFinesData = finesFileCheck()
speedFines, formattingErrorForFineRates = finesFileFormatCheck(speedFinesData)

maxSpeed = ((speedFines[-1])[1])
maxFine = ((speedFines[-1])[2])

#if formattingErrorForFineRates is True:
        ## include a option to simply create a new fine rates file in program
        #continueState = continueOrExitForFines()
        #continueOrExitDueToFormat(continueState)

#speedFileName = speedFileCheck()
#dataDict, speedFormatError = speedFileFormatCheck(speedFileName)
#if speedFormatError is True:
        #continueState = speedDataFormatError()
        #continueOrExitDueToFormat(continueState)

#carSpeeds = calculateSpeedPerHr(dataDict)
#calculateFines(carSpeeds)

#print("\n Terminal will exit in 10 seconds . . .")
#time.sleep(5)
#print("\n Terminal will exit in 5 seconds . . .")
#time.sleep(1)
#print("\n Terminal will exit in 4 seconds . . .")
#time.sleep(1)
#print("\n Terminal will exit in 3 seconds . . .")
#time.sleep(1)
#print("\n Terminal will exit in 2 seconds . . .")
#time.sleep(1)
#print("\n Terminal will exit in 1 seconds . . .")
#time.sleep(1)
#print("\n Exiting . . .")
#time.sleep(1)
# US - Speeding Program By ZFC

#imports following modules
import sys
import time
from datetime import timedelta

#defines the following variables
speedFinesName = "fine_rates.txt"
defaultFinesData = ["1-10-30\n",
                    "11-15-80\n",
                    "16-20-120\n",
                    "21-25-170\n",
                    "26-30-230\n",
                    "31-35-300\n",
                    "36-40-400\n",
                    "41-45-510\n",
                    "46-50-630"
                    ]


tunnelLength = 2690
speedLimit = 80
warningTimeLimit = 4
warningSpeed = int(((tunnelLength / (warningTimeLimit*60))*3.6))
totalTunnelZone = tunnelLength

finesTotal = {}
dataDict = {}   
carSpeeds = {}
speeding = []
safe = []
speedFines = []


#Checks if fine rates file exists
def finesFileCheck():
        try:
                speedFinesData = open(speedFinesName, "r")
                return speedFinesData
        except FileNotFoundError:
                defaultFinesFile = open(speedFinesName, "w+")
                for fineRanges in defaultFinesData:
                        defaultFinesFile.write(fineRanges)
                defaultFinesFile.close()
                speedFinesData = open("fine_rates.txt", "r")
                print('WARNING: A FINE RATES TIME DOES NOT EXSIST!!!'
                ' A DEFAULT "FINE RATES" FILE WILL BE AUTOMATICALLY CREATED!!!!')
                time.sleep(2)
                return speedFinesData   


#Checks and validates the the format of the fines and speed ranges and alerts 
#the user if there is an error
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
                                print("WARNING!: Formatting occured in fine_rates.txt"
                                " file on line {}: {}".format(lineCounter, fines))
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
                        finesTotal[int(fine[0])] = 0
                except:
                        if fines != "\n":
                                print("Except: WARNING!: Formatting occured in fine_rates.txt"
                                " file on line {}: {}".format(lineCounter, fines))
                                time.sleep(1)
                                errorOccur = True
        return speedFines, errorOccur


#Checks if the speeding data file exists
def speedFileCheck():
        while True:
                try:
                        speedFileName = input("\nPlease input the name of the data file: ")
                        print()
                        if speedFileName == "" or speedFileName == " ":
                                print("WARNING!!! : PLEASE DO NOT LEAVE BLANK!!!\n")
                                continue
                        speedFileData = open(speedFileName, "r")
                        speedFileData.close()
                        return speedFileName

                except FileNotFoundError:
                        print('WARNING!! This data file called "{}" does NOT EXIST!!'
                              .format(speedFileName))
                        print("Please check your file name or enter another file name.")
                        print("Make sure the file is in the correct directory!")


#Checks and validates the the format of the speed data and alerts 
#the user if there is an error
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
                        for lineData in dataLines:
                                speedFileLineCounter += 1
                                if lineData == "\n" or lineData == "" or lineData == " ":
                                        continue
                                if lineData in errorCarData:
                                        continue                                
                                try:    
                                        data = lineData.replace(" ","")
                                        dataKey, dataValue = data.split(",")
                                        dataValue = ((dataValue.split("\n"))[0])
                                        temp1, temp2, temp3 = dataValue.split(":")
                                        checkValue = dataValue.replace(":", "")
                                except:
                                        print("iWARNING!!! Error occurred on line {}: {}"
                                              .format(speedFileLineCounter, data))
                                        speedFormatError = True
                                        errorCarData.append(lineData)  
                                        continue
                                if (int(checkValue) is False) or len(checkValue) != 6:
                                        print("WARNING!!! Error occurred on line {}: {}"
                                              .format(speedFileLineCounter, data))
                                        speedFormatError = True
                                        errorCarData.append(dataKey)
                                        continue
                                if dataKey not in dataDict.keys():
                                        dataKey = dataKey
                                        dataDict.setdefault(dataKey, [])
                                        dataDict[dataKey].append(dataValue)
                                else:
                                        dataDict[dataKey].append(dataValue)
                                
                        return dataDict, speedFormatError
                except:
                        print("\nExcept: WARNING!!! Error occurred on line {}: {}"
                              .format(speedFileLineCounter, lineData))
                        #print(errorCarData)
                        speedFormatError = True
                        speedFileLineCounter = 0
                        errorCarData.append(lineData)


#This function prints a warning to the user if the formatting is correct for the fines
#If there is an error Asks for whether the user wants to continue or not
def continueOrExitForFines():
        print("#=#=#=#=# !!!PLEASE READ!!! #=#=#=#=#\n")
        print("Formatting Error occurred on the lines presented above. These errors have been REMOVED")
        print("Please Correct the formatting before running this program again.")
        print("You can also choose to delete the 'fine_rates.txt' file and the")
        print("program will automatically create a new one for you.")
        print("The default format is for range of fine rates is: MinSpeed-MaxSpeed-FineAmount\n")
        print("However, you can also choose to continue but the program may not work as intended\n")
        while True:
                try:
                        print("\nWould you like to continue or exit the program")
                        print("WARNING!: Continuing may not work as intended! ie missing values / calculations")
                        continueState = (input("Type STOP to exit or CONTINUE to continue the calculations: ")).lower()
                        if continueState == "stop" or continueState == "s":
                                return False
                        elif continueState == "continue" or continueState == "c":
                                return True
                        elif continueState == "" or continueState == " ":
                                print("Nothing was entered\n")
                        else:
                                print("\nInvalid Input")
                except:
                        print("Invalid Input")


#This function prints a warning to the user if the formatting is correct for the speeding data
#If there is an error: Asks for whether the user wants to continue or not
def speedDataFormatError():
        print("=========================================================================================")
        print("Formatting Error occurred on the lines presented above. These errors have been REMOVED!")
        print("Please Correct the formatting for the above data before choosing to run this file again.")
        print("The default format is for an speed entry is;  {Registration},HH:MM:SS\n")
        print("However, you can also choose to continue but the program may not work as intended:")
        print("ie. missing entries / miss calculations")
        while True:
                try:
                        print("\nWould you like to continue or exit the program")
                        print("WARNING!: Continuing may not work as intended! ie entries / calculations")
                        continueState = (input("Type STOP to exit or CONTINUE to continue the calculations: ")).lower()
                        if continueState == "stop" or continueState == "s":
                                return False
                        elif continueState == "continue" or continueState == "c":
                                return True
                        elif continueState == "" or continueState == " ":
                                print("\nNothing was entered\n")
                        else:
                                print("\nInvalid Input")
                except:
                        print("Invalid Input")


# Decides exits the program if the user chooses to or prints warning if user chooses to continue
def exitDueToFormat(continueState):
        if continueState is False:
                print("\nOperation Cancelled! . . .")
                time.sleep(2)
                
        if continueState is True:
                print("\nContinuing Program: WARNING!: Continuing may not work as intended!\n")
                time.sleep(2)
                
                
# Calculates the time difference between the exit and entry time for each car and saves it in a dict
# Then converts it into a datetime object with the total_seconds() function to get the difference in seconds
# Finds the speed in m/s and converts it to km/hr and prints appropriate warnings (if any)
def calculateSpeedPerHr(dataDict):
        carSpeeds = {}
        for data in dataDict.keys():
                if len(dataDict[data]) < 2:
                        if len(dataDict[data]) == 0:
                                print("WARNING!!! Car with unknown Plate has entered/exited at"
                                      .format(dataDict[data]))
                                continue
                        print("WARNING!!! Car: {} has been reported to NOT have exited tunnel"
                              " OR DATA IS INCORRECT!!!".format(data))
                        continue
                
                entryTime = ((dataDict[data])[0])
                exitTime = ((dataDict[data])[1])
                if entryTime == exitTime:
                        print("{} WARNING!!! : ERROR: ENTRY TIME IS THE SAME AS THE EXIT TIME! "
                              .format(data))
                        continue
                entryTimeSplit = entryTime.split(":")
                exitTimeSplit = exitTime.split(":")
                entryTimeInSec = timedelta(hours=int((entryTimeSplit[0])), 
                                           minutes=int((entryTimeSplit[1])), 
                                           seconds=int((entryTimeSplit[2])))
                exitTimeInSec = timedelta(hours=int((exitTimeSplit[0])), 
                                          minutes=int((exitTimeSplit[1])), 
                                          seconds=int((exitTimeSplit[2])))
                differenceInTime = (exitTimeInSec.total_seconds() - entryTimeInSec.total_seconds())
                metersPerSecond = totalTunnelZone / differenceInTime
                kmPerHour = (metersPerSecond * 3600) / 1000
                kmPerHour = int(kmPerHour)
                carSpeeds[data] = kmPerHour
        return carSpeeds


#Calculates the fines for each car and prints out their respective fines and warnings
def calculateFines(dataDict, carSpeeds, maxSpeed, maxFine):
        ticketCounter = 0
        for fine in finesTotal:
                finesTotal[fine] = 0
        print("\n====================================================")
        print("                      Raw Data:                     ")
        print("====================================================\n")
        for carPlate in carSpeeds.keys():
                #loops through a list of speed ranges
                for speedRange in speedFines:
                        speed = (carSpeeds[carPlate] - speedLimit)
                        speedRangeMin = speedRange[0]
                        speedRangeMax = speedRange[1]
                        if (speed <= speedRangeMax) and (speed >= speedRangeMin):
                                carFine = speedRange[2]
                                print("{} speed is {} km/hr so fine is ${}"
                                      .format(carPlate, carSpeeds[carPlate], carFine))
                                continue
                if ((speed + 80) * -1) > 0:
                        print("WARNING!!! Car: {} EXIT TIME IS LATER THAN ENTRY TIME "
                              "(Potential data error)".format(carPlate))
                        continue
                if (speed + 80) <= warningSpeed:
                        print("WARNING!!! Car: {} has was in the tunnel for more than {} minutes"
                              .format(carPlate, warningTimeLimit))  
                        continue
                if (speed <= 0):
                        carFine = None
                        print("{} speed is {} km/hr so fine is {}"
                              .format(carPlate, carSpeeds[carPlate], carFine))
                if speed > maxSpeed:
                        print("{} speed is {} km/hr so fine is ${}"
                              .format(carPlate, carSpeeds[carPlate], maxFine))
                continue
        
        #prints out all the tickets issued and warnings (if any)
        print("\n====================================================")
        print("               Tickets Issued + WARNINGS :          ")
        print("====================================================\n")
        for carPlate in carSpeeds.keys():
                for speedRange in speedFines:
                        speed = (carSpeeds[carPlate] - speedLimit)
                        speedRangeMin = speedRange[0]
                        speedRangeMax = speedRange[1]
                        if (speed <= speedRangeMax) and (speed >= speedRangeMin):
                                ticketCounter += 1
                                carFine = speedRange[2]
                                finesTotal[carFine] = finesTotal[carFine] + 1
                                print("{} Entry Time: {}, Exit Time: {}, Speed: {} KM/HR, fine: ${}"
                                .format(carPlate, dataDict[carPlate][0], dataDict[carPlate][1], carSpeeds[carPlate], carFine))
                                continue
                if ((speed + 80) * -1) > 0:
                        print("WARNING!!! Car: {} EXIT TIME IS LATER THAN ENTRY TIME "
                              "(Potential data error)".format(carPlate))
                        continue
                if (speed + 80) <= warningSpeed:
                        print("WARNING!!! Car: {} has was in the tunnel for more than {} minutes"
                              .format(carPlate, warningTimeLimit))  
                if speed > maxSpeed:
                        ticketCounter += 1
                        finesTotal[maxFine] = finesTotal[maxFine] + 1
                        print("{} Entry Time: {}, Exit Time: {}, Speed: {} KM/HR, fine: ${}"
                                .format(carPlate, dataDict[carPlate][0], dataDict[carPlate][1], carSpeeds[carPlate], maxFine))
                continue        
        
        #prints out all tickets Issued (if any) as well as the total amount of fines etc.
        if ticketCounter == 0:
                print("\nNo Speeding Cars Found -- > No Tickets Generated\n")
        else:   
                print("\nTotal Tickets Issues and Amount:")
                totalFineAmount = 0
                totalTickets = 0
                totalForFine = 0
                for fine in finesTotal:
                        totalTickets += finesTotal[fine]
                        totalForFine = fine * finesTotal[fine]
                        totalFineAmount += totalForFine
                        print("Fine: ${}, No. Of Tickets: {}, Total Fines for this fine amount: ${}"
                              .format(fine, finesTotal[fine], totalForFine))
                print("\nTotal Number of tickets Issued: {} Tickets Issued".format(totalTickets))
                print("Total Fine Amount: ${}".format(totalFineAmount))
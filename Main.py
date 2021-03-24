import sys
import time
from SpeedingModules import *


speedFinesData = finesFileCheck()
speedFines, formattingErrorForFineRates = finesFileFormatCheck(speedFinesData)

maxSpeed = ((speedFines[-1])[1])
maxFine = ((speedFines[-1])[2])

if formattingErrorForFineRates is True:
        # include a option to simply create a new fine rates file in program
        continueState = continueOrExitForFines()
        exitDueToFormat(continueState)

def speedDataLoop():
        while True:
                continueState = True
                speedFileName = speedFileCheck()
                dataDict, speedFormatError = speedFileFormatCheck(speedFileName)
                if speedFormatError is True:
                        continueState = speedDataFormatError()
                        exitDueToFormat(continueState)
                        if continueState is False:
                                return
                
                carSpeeds = calculateSpeedPerHr(dataDict)
                calculateFines(carSpeeds, maxSpeed, maxFine)
                return

while True:
        try: 
                activeState = input("\nPress ENTER to start program or type EXIT to end program: ")
                activeState = activeState.lower()
                if activeState == "":
                        speedDataLoop()
                elif activeState == "exit" or activeState == "e":
                        print("Exiting Program . . .")
                        time.sleep(2)
                        break
                else:
                        print("\nInvalid input ! ! !")
                        
        except:
                print("\nExcept: Invalid Input ! ! !")

sys.exit()
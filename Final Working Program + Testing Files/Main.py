#MAIN PROGRAM
#US Speeding Program by ZFC

import sys
import time
from SpeedingModules import *

#initalises the fines data
#checks for whether a fine file exists or not, if not it automatically creates a new one.
speedFinesData = finesFileCheck()
speedFines, formattingErrorForFineRates = finesFileFormatCheck(speedFinesData)

#Sets the max speed and max fine
maxSpeed = ((speedFines[-1])[1])
maxFine = ((speedFines[-1])[2])

#if there is an formatting Error then it alerts the user
#asks if they would like to continue to abort if there is error
if formattingErrorForFineRates is True:
        # include a option to simply create a new fine rates file in program
        continueState = continueOrExitForFines()
        exitDueToFormat(continueState)

# main program loop after initalisation
# checks that the entered file name actually exists and alerts the user if it doesn't
# checks for formatting errors and alerts the user if any.
# does calcuations and prints out all fines etc through the below functions and 
# prints out any warnings and errors

def speedDataLoop():
        try:
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
        except:
                print("An unknown error occurred")
        
# start program or exit program loop with error checking
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
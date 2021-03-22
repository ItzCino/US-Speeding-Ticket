from Speeding import *

#speedFinesData = finesFileCheck()
#speedFines, formattingErrorForFineRates = finesFileFormatCheck(speedFinesData)

#maxSpeed = ((speedFines[-1])[1])
#maxFine = ((speedFines[-1])[2])

if formattingErrorForFineRates is True:
        # include a option to simply create a new fine rates file in program
        continueState = continueOrExitForFines()
        continueOrExitDueToFormat(continueState)

speedFileName = speedFileCheck()
dataDict, speedFormatError = speedFileFormatCheck(speedFileName)
if speedFormatError is True:
        continueState = speedDataFormatError()
        continueOrExitDueToFormat(continueState)

carSpeeds = calculateSpeedPerHr(dataDict)
calculateFines(carSpeeds)
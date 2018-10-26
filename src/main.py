import os, math, operator, sys
import supportFunctions as sF


# Order in which files are given to Python
inputFileName    =   1
outputFileName1  =   2
outputFileName2  =   3
cutOff           =   10


ParsedData       =   sF.readDataGetDict()
# # # Structure for input data storage
# # # 		#totalCertified: Total number of certified applications
# # # 
# # # 		#JobTitle Dictionary
# # # 		#		#jobtitle: freqCert
# # # 
# # # 		#Work State Dictionary
# # # 		#		#workState: freqCert


	
# Put Unique Jobs and States in array for sorting
TitleList    =   [str(s) for s in ParsedData['SocName']]
StateList    =   [str(s) for s in ParsedData['WorkState']]


# Use Merge Sort to sort the keys in descending order
sortedTitleList  =  sF.mergeSort(TitleList, ParsedData['SocName'])
sortedStateList  =  sF.mergeSort(StateList, ParsedData['WorkState'])



# Write content of Job to string for output
WriteData        =   'TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n'
keyValue         =   'SocName'
for rows in sortedTitleList:
	if rows != '' and sortedTitleList.index(rows) < cutOff:
		# rows = '' + rows
		WriteData +=  '{:1s}'.format(rows) + ';'+ '{:1d}'.format(ParsedData[keyValue][rows]) + ';'+ '{:1.1f}'.format(100*ParsedData[keyValue][rows]/ParsedData['totalCertified']) + '%\n'
# Write content of Job to file
WriteFile     =  open(sys.argv[outputFileName1], 'w')
WriteFile.write(WriteData)
WriteFile.close()


# Write content of State to string for output
WriteData        =   'TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n'
keyValue         =   'WorkState'
for rows in sortedStateList:
	if rows != '' and sortedStateList.index(rows) < cutOff:
		WriteData +=  '{:1s}'.format(rows) + ';'+ '{:1d}'.format(ParsedData[keyValue][rows]) + ';'+ '{:1.1f}'.format(100*ParsedData[keyValue][rows]/ParsedData['totalCertified']) + '%\n'
# Write content of State to file
WriteFile     =  open(sys.argv[outputFileName2], 'w')
WriteFile.write(WriteData)
WriteFile.close()
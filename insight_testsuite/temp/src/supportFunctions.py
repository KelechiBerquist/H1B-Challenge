import os, math, sys, json



States         =  {}
StatesCities   =  {}
Columns        =  {}

def getUnitedStates ():
	global States       
	global StatesCities 


	with open(os.path.join(os.path.dirname(__file__), 'states_hash.json')) as thisFile:
		States = json.load(thisFile)
	

	with open(os.path.join(os.path.dirname(__file__), 'US_States_and_Cities.json')) as thisFile:
		StatesCities = json.load(thisFile)

	for state in StatesCities:
		StatesCities[state] = set(StatesCities[state])
# 
# 
# 
# 
def readDataGetDict ():
	global States       
	global StatesCities 
	global Columns 

	getUnitedStates ()

	# Order in which files are given to Python
	inputFileName    =   1
	outputFileName1  =   2
	outputFileName2  =   3

	# Read content of input files
	ReadFile         =   open(sys.argv[inputFileName], 'r')
	ThisFile         =   ReadFile.readlines()
	Header           =   ThisFile[0].strip('\n').split(';')

	Columns          =   findRelevantColumns (Header, [['STATUS'], ['SOC', 'NAME'], ['WORK', 'STATE']])
	InputData        =   { 
		'totalCertified': 0, 
		'WorkState':{}, 
		'SocName': {}
		}


	# # Put content of file into dictionary
	for line in ThisFile[1:]:
		Line   =  line.strip('\n').split(';') 
		addLine (Line, InputData)

	return InputData 

# 
# 
# 
# 
def printLines (Array, Lines):
	count = 0
	for row in zip(Array):
		count +=1
		if count < Lines:
			print(row)
# 
# 
# 
# 
def isPermutation (LongString, ShortString):
	charFreq = {}
	for i in LongString:
		if i in charFreq:
			charFreq[i] += 1
		else:
			charFreq[i] = 1

	for i in ShortString:
		charFreq[i] -= 1
		if charFreq[i] < 0:
			return False

	return True
# 
# 
# 
# 
def isSubstring (LongString, ShortString):
	checkString  =  LongString
	countIndx    =  0

	for i in checkString:
		if countIndx == len(ShortString)-1:
			return True

		if i ==  ShortString[countIndx]:
			countIndx   +=  1
		else:
			countIndx    =  0
	return False
# 
# 
# 
# 
def findRelevantColumns (Headers, SearchKeys):
	indxList    =  {}
	keyNames    =  ['status', 'socName', 'workState']
	checkTruth  =  False
	
	for fullKey in SearchKeys:
		for header in Headers:
			if SearchKeys.index(fullKey) == 0:
				checkTruth  =  isSubstring (header, fullKey[0])
			else:
				check1      =  isSubstring (header, fullKey[0])
				check2      =  isSubstring (header, fullKey[1])
				checkTruth  =  check1 and check2

			if checkTruth:
				indxList[keyNames[SearchKeys.index(fullKey)]] = Headers.index(header)
				break

	return indxList
# 
# 
# 
# 
def putInDict(grandLevel2, grandLevel1, InputData):
	# If grandLevel2 exists in grandLevel1 dictionary update its information.
	if grandLevel2 in InputData[grandLevel1]:
		InputData[grandLevel1][grandLevel2] += 1
	else:
		InputData[grandLevel1][grandLevel2] = 1
# 
# 
# 
# 
def addLine (Line, InputData):
	global States       
	global StatesCities 
	global Columns 

	# Increase the count of certified applications
	if (Line[Columns['status']] == 'CERTIFIED'):
		InputData['totalCertified'] += 1


		# If the job title exists in SocName dictionary update its information.
		putInDict(Line[Columns['socName']].replace('"', ''), 'SocName', InputData)	
			

		# If the work state exists in dictionary update its information.
		if Line[Columns['workState']]  in States:
			putInDict(Line[Columns['workState']], 'WorkState', InputData)

		else:
			# Check if work state is displaced by 2
			for indx in [-2, -1, 1, 2]:
				realIndx = Columns['workState'] + indx
				if Line[realIndx]  in States:
					putInDict(Line[realIndx], 'WorkState', InputData)
# 
# 
# 
# 
def mergeSort(toSort, theDict):
	# base case: if list size becomes less than 2 in the recursion, return the list to the higher level heap.
	if len(toSort) < 2:
		return toSort

	# recursively sort the content of the list
	theSlice  =  int(math.ceil(len(toSort)/2))
	LHS       =  mergeSort(toSort[:theSlice:], theDict)
	RHS       =  mergeSort(toSort[theSlice:], theDict)
	
	# join the returned lists from the recursive file into a master list that will be returned.
	sL = []
	while len(LHS) and len(RHS):
		if int(theDict[LHS[0]]) > int(theDict[RHS[0]]):
			sL.append(LHS.pop(0))
		elif int(theDict[LHS[0]]) < int(theDict[RHS[0]]):
			sL.append(RHS.pop(0))
		# If the frequency is equal, sort according to the key
		else:
			string1   =  LHS[0]
			string2   =  RHS[0]
			theMin    =  min( len(string1), len(string2) )
			for i in range(theMin):
				if ord(string1[i]) < ord(string2[i]):
					sL.append(LHS.pop(0))
					break

				elif ord(string1[i]) > ord(string2[i]):
					sL.append(RHS.pop(0))
					break

				elif i == theMin-1:
					if theMin  ==  len(string1):
						sL.append(LHS.pop(0))
					else:
						sL.append(RHS.pop(0))

	sL.extend(LHS)
	sL.extend(RHS)
	return sL

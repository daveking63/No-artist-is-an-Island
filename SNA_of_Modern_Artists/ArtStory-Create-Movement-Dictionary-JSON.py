import re
import json
import pickle

def loadPickleDict(pickleFileName):
    fileobj = open(pickleFileName, 'rb')
    tempDict = pickle.load(fileobj)
    fileobj.close()
    return tempDict

def dumpPickleDict(pickleFileName, dictObj):
    fileObj = open(pickleFileName, 'wb')
    pickle.dump(dictObj, fileObj)
    fileObj.close()
    
def writeJsonToFile(jFile, jObj):
    with open(jFile, 'w') as fOut:
        json.dump(jObj, fOut)
        
def readJsonFromFile(jFile):
    with open(jFile, 'r') as fIn:
        jObject = json.load(fIn)
    return jObject

def createMovementCountryDictionary(moveCountryFile):
    with open(moveCountryFile) as f:
        data = f.read()  
        f.close()    
    moveCountries = data.split("####")[1:-1]
    moveCountryDict = {}
    for movement in moveCountries:
        moveLines = movement.split('\n')
        i = 0
        for move in moveLines:
            if move != '':
                # print(i, move)
                if i == 1:
                    country = move[3:]
                else:
                    print(move,",",country)
                    if move not in moveCountryDict.keys():
                        moveCountryDict[move] = [country]
                    else:
                        moveCountryDict[move] = moveCountryDict[move] + [country]
            i += 1
    return moveCountryDict

def createMovementDict(moveDetailsFile,moveCountryDict):
    with open(moveDetailsFile) as f:
        data = f.read()  
        f.close()
    movements = data.split("####")[1:-1]
    moveCnt = 0
    movementDict = {}
    for movement in movements[0:]:
        moveFeatures = movement.split('\n')
        i = 0
        aList = []
        hList = []
        mId = moveCnt
        for line in moveFeatures:
            if re.search("^0-", line):
                mName = line[2:]
                print("'mName': ", mName)
                mTextName = mName
                movementDict[mName] = {}
                movementDict[mName]['mTextName'] = mTextName
                movementDict[mName]['_id'] = mId
                print("'_id': ", mId)
            elif re.search("^1-", line):
                mOrigID = line[2:]
                print("'mOrigID': ", mOrigID)
                movementDict[mName]['mOrigID'] = mOrigID           
            elif re.search("^2-", line):
                mILink = line[2:]
                print("'mILink': ", mILink)
                movementDict[mName]['mILink'] = mILink
            elif re.search("^3-", line):
                print("'mStartYr': ", line[2:])
                movementDict[mName]['mStartYr'] = str(line[2:])
            elif re.search("^4-", line):
                print("'mEndYr': ", line[2:])
                movementDict[mName]['mEndYr'] = line[2:]
            elif re.search("^5-", line):
                aList = aList + [line[2:]]
            elif re.search("^6-", line):
                hList = hList + [line[2:]]    
        print("'mArtists': ", aList)
        movementDict[mName]['mArtists'] = aList
        print("'mArtistLinks': ", hList)
        movementDict[mName]['mArtistLinks'] = hList
        if mName in moveCountryDict.keys():
            moveCountries = moveCountryDict[mName]
            movementDict[mName]['mCountries'] = moveCountries
            print("'moveCountries': ", moveCountries)
        else:
            print('***No countries')
        moveCnt += 1
    return movementDict

# Main

# Set up the relationship between movements and their countries of origin.
# Originally, found in Artstory listings of movements by country and stored locally in a file
# that lists countries with their movements. This file is read and first converted to a set of
# entries whose format is 'movement,country'.  The converted file is then stored in a dictionary 
# with the movement names as keys and the values consisting of a list of countries.
# E.g. 'Fluxus': ['American', 'Japanese'] which indicates Fluxus was originated in America and Japan. 

path = 'C:/Research/Artstory/'
moveByCountry = 'Artstory-Movements-by-Country-July-2018.txt'
moveCountryFile = path + moveByCountry
moveCountryDict = createMovementCountryDictionary(moveCountryFile)

# Create dictionary for artistic movements from Artstory.Org.  Individual movement pages
# were originally downloaded, stored,and scraped with the initial details for all the movements
# stored in a single local file with the following data for each movement:  0-name, 1-_id, 2- orig id; 
# 3- year started, 4-year ended, 5-main artists associated with movement, 
# 6-links to either Artstory pages devoted to the artist or other source pages, 
# and a list of countries # where movement originated. This data was then used to create a python dictionary.

# read in other feature details and combine with moveCountryDict
path = 'C:/Research/Artstory/'
#  
moveDetails = 'ArtStory-Movements-All-tempDetails-July-2018.txt'
moveDetailsFile = path + moveDetails
movementDict = createMovementDict(moveDetailsFile, moveCountryDict)

# save dictionaries in pickle file
pickleFile = path + 'movementDictPickle'
dumpPickleDict(pickleFile, movementDict)

pickleFile2 = path + 'movementCountryDict'
dumpPickleDict(pickleFile2, moveCountryDict)

#Add alternative JSON format
movementJson = json.dumps(movementDict)

#Save and load JSON object to and from a file

jFile = path + 'Artist-movementJson4.txt'
writeJsonToFile(jFile, movementJson)

# Read saved JSON object from file -- readJsonFromFile produces a string
# The string is converted into a dictionary by doing a json.load on the string

movementJsonTemp = readJsonFromFile(jFile)
movementJsonDict = json.loads(movementJsonTemp)
movementJsonDict.keys() # check validity of json.loads

# Print version of Json -- "indent" and "sort_keys" are variables
movementJsonPrint = json.dumps(movementDict, indent = 2, sort_keys = True)
print(movementJsonPrint)
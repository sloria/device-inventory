# @see <a href="http://en.wikipedia.org/wiki/Verhoeff_algorithm/">More Info</a>
# @see <a href="http://en.wikipedia.org/wiki/Dihedral_group">Dihedral Group</a>
# @see <a href="http://mathworld.wolfram.com/DihedralGroupD5.html">Dihedral Group Order 10</a>

# Adapted from code originally by Hermann Himmelbauer
# Author Rick Solis 

#http://en.wikipedia.org/wiki/Verhoeff_algorithm

# generates subect id using the following format
# 0000-1-22-3
# 0: subj id
# 1: time point for data collection
# 2: session: cohort group
# 3: Subj ID check digit

from verhoeff import *
#import gdata.docs.service
#import gdata.spreadsheet.text_db
#from gdataClientSettings import * 

#### EXPERIMENT SETTINGS ####
# TODO
# Move these settings to an external file 
session = 1
timepoint = 1
totalSubjects = 23
dbName = 'ecwell-pilot'
subjectTable = 'subjects'
deckTypeList = {'orange':0, 'purple':1}
ticketValues = range(1,11)
ticketTableName = 'tickets'
#############################


def generate(number, timepoint, session, lastsubid = None):
    # generates subect id using the previously described format. 
    
    # num: Number of ids to generate
    
    # lastsubid: last subect id generated. used as a starting point.
    # if not specified, generated ids start at 0001.

    # Returns an array of subject ids 
    lastsub='0001'
    subidList=[]
    
    if timepoint >3:
        raise Exception("Time point is greater than 3")
    if session > 10: 
        raise Exception("Session is greater than 10")
    
    if lastsubid:
        if not validate(lastsubid):
            raise Exception("invalid last sub id")
        else:
            lastsub = str(int(lastsubid[:4]) + 1)
    for num in range(int(lastsub[:4]), number+int(lastsub[:4]), 1):
        #x = str(format(num, "04d"))+'-'+str(timepoint)+'-'+str(format(session, "02d"))+ '-'+str(calcsum(format(num, "04d")+str(timepoint)+format(session, "02d")))
        
        #Build the subject number (minus the check digit)
        subNum = str(format(num, "04d"))+'-'+str(timepoint)+'-'+str(format(session, "02d"))
        
        #Calculate the check digit for the subject number
        checkDigit = str(calcsum(subNum.replace('-', '')))
		
        #Combine together for final subject number 
        subjectID = subNum + '-' + checkDigit
        assert validate(subjectID) == True
        
        subidList.append(subjectID)
    return subidList
    
def validate(number):
    """Validate subect id checksummed number (checksum is last digit)"""
    num = number.replace('-', '')
    return checksum(num) == 0
    
def getID(id):
    sub = id.replace('-','')
    return sub[0:4]
    
def getTimePoint(id):
    sub = id.replace('-','')
    return sub[4:5]

def getSession(id):
    sub = id.replace('-','')
    return sub[5:7]

def getCheckDigit(id):
    sub = id.replace('-','')
    return sub[7:8]

def formatID(id):
    return getID(id) + '-' + getTimePoint(id) + '-' + getSession(id) + '-' + getCheckDigit(id)

def validateID(subdb, id):
    myclient = gdata.spreadsheet.text_db.DatabaseClient(email, password)

    # Get the first database with the matching name .. Hopefully there's only one. 
    mydb = myclient.GetDatabases(name = subdb)
    ecwellDB  = mydb[0]

    #Get the first table containing the subject ids, should only be one 
    #GetTables() returns an array, so we index for the first table 
    subtable = ecwellDB.GetTables(name=subjectTable)[0]

    myquery = 'session = ' + str(session)

    #Find the subjects for the matching session 
    subrecords = subtable.FindRecords(myquery)
    mysubList = []
    for rec in subrecords:
        mysubList.append(rec.content['subid'])
    return id in mysubList
# Some tests and also usage examples


idList = generate(70, 0, 1) 

  
#Examples 
#generate(20, 1, 2, lastsubid = '019-1-02-7')
#generate(20, 1, 2, lastsubid = '038-1-02-8')
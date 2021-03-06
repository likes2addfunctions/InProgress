import mysql.connector

cnx = mysql.connector.connect(user='root', password='',
                              host='127.0.0.1',
                              database='gf_data')


def getDataRange(startDate,startHour, startMin, \
                endDate, endHour, endMin,\
                symbol):
    querystr = "select time_gathered, pr, cp from masterdata where " \
               + "symbol = '" + symbol \
               + "' and " + startDate + " <= time_gathered <= " + endDate \
               + " and hour(time_gathered) <= " + endHour \
               + " and " + startHour + " <= hour(time_gathered) " \
               + " and minute(time_gathered) <= " + endMin \
               + " and " + startMin + " <= minute(time_gathered) ;" 
    #print querystr             
    query = (querystr)
    cursor = cnx.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    return data

def getDataLater(startDate,startHour, startMin, \
                endDate, endHour, endMin,\
                symbol, delta):
    querystr = "select time_gathered, pr from masterdata where " \
               + "symbol = '" + symbol \
               + "' and " + startDate + " <= time_gathered <= " + endDate \
               + " and hour(time_gathered) <= " + str(endHour +delta)\
               + " and " + str(startHour + delta) + " <= hour(time_gathered) " \
               + " and minute(time_gathered) <= " + str(endMin) \
               + " and " + str(startMin) + " <= minute(time_gathered) ;"
    #print querystr             
    query = (querystr)
    cursor = cnx.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
##    for (time_gathered, pr) in cursor:
##        print [time_gathered, pr.format()]
    #for (time_gathered, pr) in data:
#        z = time_gathered.hour
#        
#        print z
#        print "{} {}".format(time_gathered, pr)
    return data

##getDataRange("2017-02-08", "06", "57", \
##            "2017-02-08", "12", "59", \
##            "AMD")
##
##z = getDataLater("2017-02-08", 06, 57, \
##            "2017-02-08", 12, 59, \
##            "AMD",2)
##print z[0]

def getHour(entry):
    return entry[0].hour

##getHour(z[0])

def cleanVarChar(data):
    formattedData = []
    for row in data:
        formattedRow = []
        for entry in row:
            formattedRow = formattedRow + [float(entry)]
        formattedData = formattedData + [formattedRow]
    print formattedData
    return formattedData

def addPChange(data):
    newData = []
    for row in data:
        row[0] = (row[0] - row[1])/row[0]
        newData = newData + [row]
    return newData

def makeDataforGD(delta):
    result = []
    currentData = getDataRange("2017-02-08", "06", "57", \
            "2017-02-08", "12", "59", \
            "AMD")

    laterData = getDataLater("2017-02-08", 06, 57, \
            "2017-02-08", 12, 59, \
            "AMD",delta)
    for i in range(len(currentData)):
        A = getHour(currentData[i])
        try:
            B = getHour(laterData[i])
        except:
            B = 9999
        #print A, B
        if A+1 == B:
            
            entry = [laterData[i][1]] + list(currentData[i][1:])
            #print entry
            result = result + [entry]
    result = cleanVarChar(result)
    result = addPChange(result)
    print result
    return result

makeDataforGD(1)       



cnx.close()



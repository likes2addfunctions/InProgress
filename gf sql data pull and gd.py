import mysql.connector
import random
import numpy
import matplotlib.pyplot as plt
import plotly.plotly as py
	

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

Data = makeDataforGD(1)       

cnx.close()

NumOfVars = len(Data[0]) - 1
   

### Linear Regression Hypothesis
Theta_naught = [0]
for i in range(NumOfVars):
    Theta_naught = Theta_naught + [1]
Theta_naught = numpy.array(Theta_naught)

def hTheta(Theta, x):
    return Theta[0] + numpy.dot(Theta[1:],x)

### Cost Function
def JTheta(Theta, Data):
    cost = 0
    for k in range(len(Data)):
        x = []
        for j in range(NumOfVars):
            x = x + [Data[k][j+1]]
        cost = cost + (hTheta(Theta,x) - Data[k][0])**2
    cost = cost/(2*NumOfVars)    

### Run Gradient Descent


def GradDescent(Theta,Data,a, iterations):
    Thetas = []
    for i in range(iterations):
        DJ0 = 0
        for k in range(len(Data)):
            x = []
            for j in range(NumOfVars):
                x = x + [Data[k][j+1]]
            DJ0 = DJ0 + (hTheta(Theta,x) - Data[k][0])
        DJ0 = DJ0/(NumOfVars)
        DJ = [DJ0]
        
        for m in range(NumOfVars):
            DJm = 0
            for k in range(len(Data)):
                x = []
                for j in range(NumOfVars):
                    x = x + [Data[k][j+1]]
                DJm = DJm + (hTheta(Theta,x) - Data[k][0])*x[m]
            DJm = DJm/(NumOfVars)
            DJ = DJ + [DJm]
        DJ = numpy.array(DJ)  
        
        Theta = Theta - a*DJ
        Thetas = Thetas + [Theta[1]]
    print(len(Thetas))
    plt.plot(range(iterations), Thetas)
    #plt.plot(range(iterations), t1s)
    printstr = "y = " + str(Theta[0])
    for k in range(NumOfVars):
        printstr = printstr + " + " + str(Theta[k+1]) + "x_" + str(k+1)
    print printstr
    plt.show()

GradDescent(Theta_naught,Data,.001,1000)




### This is a tool to perform gradient descent on multiple variables.
# Based on Andrew Ng's Machine Learning course at Stanford.
# It currently generates a pseudo random input, then runs the algorithm
# and provides a hypothesis as well as a visualization of convergence.

import random
import numpy
import matplotlib.pyplot as plt
import plotly.plotly as py
import mysql.connector
import datetime
import math


symbol = "'AMD'"

cnx = mysql.connector.connect(user='g', password='g',
                              host='10.0.0.7',
                              database='gf_data')
        
querystr = "select * from masterdata where \
            time_gathered >= '2017-02-19 12:00:00' \
            and time_gathered <= '2017-02-22 08:32:56' \
            and symbol = " + symbol + " ; "
print querystr
query = (querystr)
cursor = cnx.cursor()
cursor.execute(query)


def cleanCursor(cursor):
    data = []
    mean = 0
    for entry in cursor:
        newentry = list(entry[:3])
        #indicies = range(len(entry)-3)
        indicies = range(3)
        for k in indicies:
            item = entry[k+3]
            newitem =''
            for letter in item:
                newitem = newitem + str(letter)
            try:
                newentry = newentry + [float(newitem)]
            except:
                newentry = newentry + [newitem]
        data = data + [newentry]
    return data

data = cleanCursor(cursor)

### Formatted Data will be of the form (%change in 24 hours, stats)

formattedData = []

for k in range(len(data)):
    entry = data[k]
    entrytime = entry[2]
    querytimestart = entrytime + datetime.timedelta(days=1, seconds = -30)
    querytimeend = entrytime + datetime.timedelta(days=1, seconds = 30)
    querystr  = "select * from masterdata where symbol = 'AMD' \
                    and time_gathered >= '" + str(querytimestart) + \
                    "' and time_gathered <= '" + str(querytimeend) + "' ;"
    #print querystr
    query = (querystr)
    cursor = cnx.cursor()
    cursor.execute(query)
    nextday = cleanCursor(cursor)
    if nextday != []:
        if nextday[0][4] != 'NA' and data[k][4] != 'NA':
            formattedData = formattedData + [[(nextday[0][4] - data[k][4])/data[k][4]] + data[k][3:]]

        




  
print formattedData[0:10]
##print data[-1]
##print len(data)
##print mean

cnx.close()


NumOfVars = len(formattedData[0]) - 1
print NumOfVars

Data = formattedData
    
#print XVect
#print YVect

### Create Test Set
test_set = []
indicies = []
for i in range(len(Data)/10):
    indi = random.randrange(len(Data))
    test_set = test_set + [Data[indi]]
    Data = Data[:indi] + Data[(indi +1):]

### Linear Regression Hypothesis
Theta_naught = [0]
for i in range(NumOfVars):
    Theta_naught = Theta_naught + [1]
Theta_naught = numpy.array(Theta_naught)

###Predicted value
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
    fig = plt.figure()
    plt.plot(range(iterations), Thetas)
    #plt.plot(range(iterations), t1s)
    printstr = "y = " + str(Theta[0])
    for k in range(NumOfVars):
        printstr = printstr + " + " + str(Theta[k+1]) + "x_" + str(k+1)
    print printstr
    plt.show()
    #fig.savefig('test.png')
    model = []
    for k in range(NumOfVars+1):
        model = model + [Theta[k]]
    print model
    return model


def testSetError(test_set, model):
    sqErrors = []
    successes = 0
    for entry in test_set:
        y = model[0]
        for k in range(len(entry)-1):
            y = y + (entry[k+1])*(model[k+1])
        if math.copysign(1,y) == math.copysign(1,entry[0]):
            successes = successes + 1
        error = entry[0] - y
        print entry[0], math.copysign(1,entry[0]), y, math.copysign(1,y)
        sqErrors = sqErrors + [error**2]
    #print "sqe", sqErrors
    SSE = 0
    for x in sqErrors:
        SSE = SSE + x
    print "SSE", SSE
    SD = numpy.sqrt(SSE)/(len(model) - 1)
    print "SD", SD
    print successes, "successes out of", len(test_set), "trials"
    print float(successes)/len(test_set)
    return SD
            
testSetError(test_set, GradDescent(Theta_naught,Data,.00001,100))
#
#plt.scatter(XVect,YVect)
#plt.show()






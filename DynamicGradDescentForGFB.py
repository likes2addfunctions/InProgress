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

cnx = mysql.connector.connect(user='g', password='g',
                              host='10.0.0.7',
                              database='gf_data')



def getData(symbol):

            
    querystr = "select * from masterdatab where pr is not null and " + \
                "time_gathered >= '2017-02-20 06:00:00' " + \
                "and time_gathered <= '2017-02-21 10:32:56' " + \
                "and symbol = " + symbol + " ; "
    print querystr
    query = querystr
    cursor = cnx.cursor()
    cursor.execute(query)
    return cursor


def cleanCursor(cursor):
    data = []

    for entry in cursor:
        newentry = []
        for item in entry:
            try:
                newitem = [float(item)]
            except:
                newitem = [item]
            newentry = newentry + newitem
        data = data + [newentry]
    #print data[0:2]

    return data


def formatData(data,symbol):
    formattedData = []
    for k in range(len(data)):
        entry = data[k]
        entrytime = entry[2]
        querytimestart = entrytime + datetime.timedelta(days=1, seconds = -30)
        querytimeend = entrytime + datetime.timedelta(days=1, seconds = 30)
        querystr  = "select pr from masterdatab where pr is not null and symbol = " + symbol + \
                        " and time_gathered >= '" + str(querytimestart) + \
                        "' and time_gathered <= '" + str(querytimeend) + "' ;"
        #print querystr
        query = (querystr)
        cursor = cnx.cursor()
        cursor.execute(query)
        nextday = cleanCursor(cursor)
        if len(nextday) > 0:
            #print nextday , data[k]
            formattedData = formattedData + [[(nextday[0][0] - data[k][4])/data[k][4]] + data[k][3:]]
    #print formattedData[0:2]
    return formattedData

### Create Test Set
def createTestSet(Data):
    test_set = []
    indicies = []
    for i in range(len(Data)/10):
        indi = random.randrange(len(Data))
        test_set = test_set + [Data[indi]]
        Data = Data[:indi] + Data[(indi +1):]
    return (Data, test_set)



###Predicted value
def hTheta(Theta, x):
    try:
        return Theta[0] + numpy.dot(Theta[1:],x)
    except:
        print Theta, x
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


def GradDescent(Theta,Data,a, iterations,symbol):
    Thetas = []
    maxDJs = []
    maxCount = 0
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
        maxDJs = maxDJs + [max(DJ)]
        Theta = Theta - a*DJ
        #Thetas = Thetas + [Theta[1]]
        maxCount = maxCount + 1
        if maxCount > 4*NumOfVars:
            maxDJ = 0
            for k in range(2*NumOfVars):
                maxDJ = maxDJ + maxDJs[-(k+1)]
            if maxDJ < 1:
                return printResults(maxDJs,Theta,symbol,maxCount)
            growthCount = 0
            for k in range(2*NumOfVars):
                if maxDJs[-(k+1)] > maxDJs[-(k+2)]:
                    growthCount = growthCount + 1
            #print growthCount
            if growthCount > NumOfVars - 2:
                a = a/10
                Theta_naught = [1]
                for i in range(NumOfVars):
                    Theta_naught = Theta_naught + [1]
                Theta_naught = numpy.array(Theta_naught)
                Theta = Theta_naught
                print "alpha changed to", a, "on iteration", len(maxDJs)
                print "GD restarted with new alpha"
                maxCount = 0
    return printResults(maxDJs,Theta,symbol,maxCount)
                
                
    #print(len(Thetas))
                
def printResults(maxDJs,Theta,symbol,maxCount):
    fig = plt.figure()
    offset = len(maxDJs) - maxCount
    offsetvector = []
    for item in range(maxCount):
        offsetvector = offsetvector + [offset]
    offsetvector = numpy.array(offsetvector)
    xs = numpy.array(range(maxCount))
    xs = xs + offsetvector
    #print xs
    ax1 = fig.add_subplot(211)
    #print len(xs), len(maxDJs[-maxCount:])
    plt.plot(xs, maxDJs[-maxCount:])
    ax2 = fig.add_subplot(212)
    plt.plot(range(len(maxDJs)), maxDJs)
    
    #plt.plot(range(iterations), t1s)
    maxDJ = 0
    for k in range(2*NumOfVars):
        maxDJ = maxDJ + maxDJs[-(k+1)]

    print "sum of last 2n max DJs:", maxDJ
    printstr = "y = " + str(Theta[0])
    for k in range(NumOfVars):
        printstr = printstr + " + " + str(Theta[k+1]) + "x_" + str(k+1)
    print printstr
    #plt.show()
    figtitle = symbol[1:-1] + ".png"
    fig.savefig(figtitle)
    model = []
    for k in range(NumOfVars+1):
        model = model + [Theta[k]]
    #print model
    return model


def testSetError(test_set, model):
    sqErrors = []
    successes = 0
    for entry in test_set:
        y = model[0]
        #print model, entry
        for k in range(len(model)-1):
            y = y + (entry[k+1])*(model[k+1])
        if math.copysign(1,y) == math.copysign(1,entry[0]):
            successes = successes + 1
        error = entry[0] - y
        #print entry[0], math.copysign(1,entry[0]), y, math.copysign(1,y)
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
    print " "
    print " "
    return SD

def genAndTest(symbol):
    Data = formatData(cleanCursor(getData(symbol)),symbol)
    #print Data[0:5]

    ### Linear Regression Hypothesis
    Theta_naught = [1]
    for i in range(NumOfVars):
        Theta_naught = Theta_naught + [1]
    Theta_naught = numpy.array(Theta_naught)

    testData = createTestSet(Data)

    testSetError(testData[1], GradDescent(Theta_naught,testData[0],.0001,5,symbol))

stat_list = ["cp", "pr" ,"open", "vol", "market_cap","pe_ratio", "Div", "eps", "Shares", "beta", "inst" ]

stock_list = ["'AMD'", "'F'", "'AAPL'", "'RAD'", "'CHK'", "'S'", \
              "'BAC'", "'DRYS'","'FB'"]

NumOfVars = 3

for symbol in stock_list:
    genAndTest(symbol)

    


cnx.close()




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
                "time_gathered >= '2017-03-21 06:00:00' " + \
                "and time_gathered <= '2017-03-21 12:32:56' " + \
                "and symbol = " + symbol + " ; "
    print querystr
    query = querystr
    cursor = cnx.cursor()
    cursor.execute(query)
    return cursor

def getDatapt(symbol):        
    querystr = "select * from masterdatab where " + \
                "time_gathered >= '2017-04-24 08:31:00' " + \
                "and time_gathered <= '2017-04-24 8:32:00' " + \
                "and symbol = " + symbol + " ; "
    query = querystr
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.close()
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
    #print data

    return data

#returns a list of data [%change over 24hrs, data1, data2, ...]
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
            formattedData = formattedData + [[(nextday[0][0] - data[k][4])/data[k][4]] + data[k][3:3+NumOfVars]]
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
        print (Theta, x)
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
            DJ = DJ + [abs(DJm)]
        DJ = numpy.array(DJ)  
        maxDJs = maxDJs + [max(DJ)]
        Theta = Theta - a*DJ
        Thetas = Thetas + [Theta[1]]
        if len(maxDJs) > 4:
            if maxDJs[-1] > maxDJs[-2] and maxDJs[-1] > maxDJs[-3]:
                Theta = []
                for k in range(NumOfVars+1):
                    Theta = Theta + [1]
                a = a/2
            DJsum = 0
            for k in range(4):
                DJsum = DJsum + maxDJs[-1*(k+1)]
            if DJsum < 1:
                print str(symbol), len(Thetas)
                model = []
                for k in range(NumOfVars+1):
                    model = model + [Theta[k]]
                return model
    model = []
    for k in range(NumOfVars+1):
        model = model + [Theta[k]]
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
    p = (float(successes)/len(test_set))
    model = [p] + model
    return model

def genAndTest(symbol):
    Data = formatData(cleanCursor(getData(symbol)),symbol)

    ### Linear Regression Hypothesis
    Theta_naught = [1]
    for i in range(NumOfVars):
        Theta_naught = Theta_naught + [1]
    Theta_naught = numpy.array(Theta_naught)

    testData = createTestSet(Data)

    model = [symbol] + testSetError(testData[1], GradDescent(Theta_naught,testData[0],.01,500,symbol))
    return model

stat_list = ["cp", "pr" ,"open", "vol", "market_cap","pe_ratio", "Div", "eps", "Shares", "beta", "inst" ]

stock_list = ["'DRYS'", "'AAPL'", "'RAD'", "'F'", "'CHK'", "'S'", \
              "'BAC'", "'AMD'","'FB'"]
stock_listb = ["'AMD'","'FB'"]


NumOfVars = 3

def make_current_prediction(model):
    symbol = model[0]
    currentData = formatData(cleanCursor(getDatapt(symbol)),symbol)[0]
    y = model[2]
    for k in range(len(currentData)-1):
        y = y + (currentData[k+1]*(model[k+3]))
    printstr  = "predicted change from " + str(symbol) + " is " + str(y) + "%"
    print printstr
    print "expceted:", symbol, y*model[1]
    return (symbol, y*model[1])



def compare_models(cutoff):
    Models = []
    for symbol in stock_list:
        model = genAndTest(symbol)
        if model[1] > cutoff:
            Models = Models + [model]
    print " "
    print Models
    print " "
    predictions = []
    sell = []
    buy = []
    for model in Models:
        predictions = predictions + [make_current_prediction(model)]
        print " "
    total_expectation = 0
    for Entry in predictions:
        Entry = list(Entry)
        if Entry[1] < 0:
            sell = sell + [Entry[0]]
        else:
            buy = buy + [Entry]
            total_expectation = total_expectation + Entry[1]
    for Entry in buy:
        Entry[1] = Entry[1]/total_expectation
    print "sell", sell
    print "buy", buy
        


compare_models(.7)


            










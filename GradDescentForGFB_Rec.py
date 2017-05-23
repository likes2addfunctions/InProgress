

import random
import numpy
import matplotlib.pyplot as plt
import plotly.plotly as py
import mysql.connector
import datetime
import math
import time



stat_list = ["cp", "pr" ,"open", "vol", "market_cap","pe_ratio", "Div", "eps", "Shares", "beta", "inst" ]

stock_list = ["'DRYS'", "'AAPL'", "'RAD'", "'F'", "'CHK'", "'S'", \
              "'BAC'", "'AMD'","'FB'"]
stock_listb = ["'AMD'","'FB'"]


NumOfVars = 3

cnx = mysql.connector.connect(user='g', password='g',
                              host='10.0.0.7',
                              database='gf_data')



def getData(symbol,querystr):
    #print querystr
    query = querystr
    cursor = cnx.cursor()
    cursor.execute(query)
    return cursor



def cleanCursor(cursor):
    trainsize = 200
    clst = list(cursor)
    trainset = []
    if len (clst) > trainsize:
        for j in range(trainsize):
            k = random.randrange(len(clst))
            trainset = trainset + [clst[k]]
            clst = clst[:k] + clst[(k +1):]
    else:
        trainset = clst
    data = []

    for entry in trainset:
        newentry = []
        for item in entry:
            try:
                newitem = [float(item)]
            except:
                newitem = [item]
            newentry = newentry + newitem
        data = data + [newentry]
    return data

def makeQuerystr(symbol, startdate, enddate):
    querystr = "select * from masterdatab where pr is not null and " + \
                "time_gathered >=  '" + startdate + \
                "' and time_gathered <= '" + enddate + \
                "' and symbol = " + symbol + " ; "
    return querystr

#returns a list of data [%change over 24hrs, data1, data2, ...]
def formatData(data,symbol):
    formattedData = []
    for k in range(len(data)):
        entry = data[k]
        entrytime = entry[2]
        querytimestart = entrytime + datetime.timedelta(days=1, minutes = -30)
        querytimeend = entrytime + datetime.timedelta(days=1, minutes = 30)
        querystr  = "select pr from masterdatab where pr is not null and symbol = " + symbol + \
                        " and time_gathered >= '" + str(querytimestart) + \
                        "' and time_gathered <= '" + str(querytimeend) + "' ;"
        query = (querystr)
        cursor = cnx.cursor()
        cursor.execute(query)
        nextday = cleanCursor(cursor)
        if len(nextday) > 0:
            formattedData = formattedData + [[(nextday[0][0] - data[k][4])/data[k][4]] + data[k][3:3+NumOfVars]]
    return formattedData

def formatcurrentData(data,symbol):
    formattedData = []
    for k in range(len(data)):
        formattedData = formattedData + [[1] + data[k][3:3+NumOfVars]]
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
                maxDJs = []
            else:
                DJsum = 0
                for k in range(4):
                    DJsum = DJsum + maxDJs[-1*(k+1)]

                if DJsum < .1:
                    print str(symbol), len(Thetas)
                    model = []
                    for k in range(NumOfVars+1):
                        model = model + [Theta[k]]
                    return model
    model = []
    for k in range(NumOfVars+1):
        model = model + [Theta[k]]
    print str(symbol), len(Thetas)
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

def genAndTest(symbol,startdate,enddate):
    querystr = makeQuerystr(symbol, startdate, enddate)
    Data = formatData(cleanCursor(getData(symbol,querystr)),symbol)

    ### Linear Regression Hypothesis
    Theta_naught = [1]
    for i in range(NumOfVars):
        Theta_naught = Theta_naught + [1]
    Theta_naught = numpy.array(Theta_naught)

    testData = createTestSet(Data)

    model = [symbol] + testSetError(testData[1], GradDescent(Theta_naught,testData[0],.01,500,symbol))
    return model




def make_current_prediction(model, startdate, enddate):
    symbol = model[0]
    querystr = makeQuerystr(symbol, startdate, enddate)
    currentDataA = formatcurrentData(cleanCursor(getData(symbol,querystr)),symbol)
    if len(currentDataA) == 0:
        print "no data found"
        return []
    currentData = currentDataA[0]
    y = model[2]
    for k in range(len(currentData)-1):
        y = y + (currentData[k+1]*(model[k+3]))
    printstr  = "predicted change from " + str(symbol) + " is " + str(y) + "%"
    print "expceted:", symbol, y*model[1]
    return [y*model[1],currentData[2]]



def compare_models(cutoff, date):
    Models = []
    fail = []
    trainstart = str(date + datetime.timedelta(days=-7))
    trainend = str(date + datetime.timedelta(days=-1))
    currentstart = str(date + datetime.timedelta(hours=-1))
    currentend = str(date + datetime.timedelta(hours=1))
    for symbol in stock_list:
        if get_current(symbol,currentstart,currentend):
            model = genAndTest(symbol,trainstart,trainend)
            Models = Models + [model]
    predictions = []
    sell = []
    buy = []

    for model in Models:
        predictions = predictions + [model[:2] + make_current_prediction(model,currentstart,currentend)]
    total_expectation = 0
    for Entry in predictions:
        print "Entry", Entry
        if Entry[1] > cutoff and len(Entry) > 2:
            if Entry[2] < 0:
                sell = sell + [Entry]
            else:
                buy = buy + [Entry]
                total_expectation = total_expectation + Entry[2]
        else:
            fail = fail + [Entry]
    for Entry in buy:
        Entry[2] = Entry[2]/total_expectation
    print "sell", sell
    print "buy", buy
    print "fail", fail
    return (sell, fail, buy)


def get_current(symbol, startdate, enddate):
    querystr = makeQuerystr(symbol, startdate, enddate)
    currentDataA = formatcurrentData(cleanCursor(getData(symbol,querystr)),symbol)
    if len(currentDataA) == 0:
        return 0
    return 1


def test_over_time():
    budget = 10000
    date = datetime.datetime(2017, 4, 3, 12, 31)
    #list of pairs [stock, shares]
    owned = []
    for k in range(30):
        cost = 0
        suggestions = compare_models(.75,date + datetime.timedelta(days=k))
        sell = suggestions[0]
        fail = suggestions[1]
        buy = suggestions[2] 
        sell = sell + fail + buy
        for k in range(len(owned)):
            for j in range(len(sell)):
                print owned[k][0], sell[j][0]
                if owned[k][0] == sell[j][0]:
                    budget = budget + owned[k][1]*sell[j][3]
                    owned = owned[:k] + [[0,0]]+ owned[k+1:]
                    print owned
                    print budget
        if len(sell) > 0:
            owned = []
        for k in range(len(suggestions[2])):
            percentofbudget = suggestions[2][k][2]
            price = suggestions[2][k][3]
            b = percentofbudget*budget
            numtobuy = math.floor(b/price)
            owned = owned + [[suggestions[2][k][0], numtobuy]]
            cost = cost + numtobuy*price
        budget = budget - cost
        print owned
        print budget
        print " "
            

test_over_time()               
        
        
        
        
            










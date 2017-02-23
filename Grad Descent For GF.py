### This is a tool to perform gradient descent on multiple variables.
# Based on Andrew Ng's Machine Learning course at Stanford.
# It currently generates a pseudo random input, then runs the algorithm
# and provides a hypothesis as well as a visualization of convergence.

import random
import numpy
import matplotlib.pyplot as plt
import plotly.plotly as py
import mysql.connector

	
### Generates data set of [Y, X1, X2, ... Xn], for example [Price, House Size, number of bedrooms, ...]#SampleSize = 50
cnx = mysql.connector.connect(user='g', password='g',
                              host='10.0.0.7',
                              database='gf_data')
        
querystr = "select * from masterdata where \
            time_gathered >= '2017-02-21 12:00:00' \
            and time_gathered <= '2017-02-22 08:32:56' \
            and symbol = 'AMD'; "
query = (querystr)
cursor = cnx.cursor()
cursor.execute(query)

data = []
mean = 0
for entry in cursor:
    newentry = list(entry[:3])
    #indicies = range(len(entry)-3)
    indicies = range(5)
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
        #mean = mean + newentry[3]

for entry in data[0:5]:
    entrytime = entry[2]
    querytime = str(entrytime.hour)
    querystr  = "select * from masterdata where \
                    symbol = 'AMD' \
                    and time_gathered >= " + str(entrytime) + \
                    " and time_gathered <= "
    print querystr

  
print data[0:10]
print data[-1]
##print len(data)
##print mean

cnx.close()


NumOfVars = 5

Data = []

coefs = []
for i in range(NumOfVars):
    m =  2 * random.random() - 1
    coefs = coefs + [m]
        
for i in range(500):
    point = []
    y = 0
    for k in range(NumOfVars):
        x = 2*random.random() - 1
        y = y + coefs[k]*x    
        point = point + [x]
    point = [y] + point
    Data = Data + [point]
    
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
    print coefs
    printstr = "y = " + str(Theta[0])
    for k in range(NumOfVars):
        printstr = printstr + " + " + str(Theta[k+1]) + "x_" + str(k+1)
    print printstr
    plt.show()
    fig.savefig('test.png')
    model = []
    for k in range(NumOfVars+1):
        model = model + [Theta[k]]
    return model


def testSetError(test_set, model):
    sqErrors = []
    for entry in test_set:
        y = 0
        for k in range(len(entry)-1):
            y = y + (entry[k+1])*(model[k])
        error = (entry[0] - y)/(entry[0])
        print entry[0], y, error
        sqErrors = sqErrors + [error**2]
    #print "sqe", sqErrors
    SSE = 0
    for x in sqErrors:
        SSE = SSE + x
    print "SSE", SSE
    SD = numpy.sqrt(SSE/(len(model) - 1))
    print "SD", SD
    return SD
            
#testSetError(test_set, GradDescent(Theta_naught,Data,.01,100))
#
#plt.scatter(XVect,YVect)
#plt.show()






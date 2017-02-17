### This is a tool to perform gradient descent on multiple variables.
# Based on Andrew Ng's Machine Learning course at Stanford.
# It currently generates a pseudo random input, then runs the algorithm
# and provides a hypothesis as well as a visualization of convergence.
import sys
import random
import numpy
import matplotlib.pyplot as plt
import plotly.plotly as py
import datetime
	
### Generates data set of [Y, X1, X2, ... Xn], for example [Price, House Size, number of bedrooms, ...]#SampleSize = 50
def createData(NumOfVars):
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
    return (Data,coefs)
    

### Linear Regression Hypothesis


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

def getMaxDiff(lst):
    maxDiff = 0
    for k in lst:
        for m in lst:
            if abs(k-m) > maxDiff:
                maxDiff = abs(k-m)
    return maxDiff

### Run Gradient Descent


def GradDescent(Data, coefs, a, iterations, NumOfVars, testno):
    Theta_naught = [0]
    for i in range(NumOfVars):
        Theta_naught = Theta_naught + [1]
    Theta = numpy.array(Theta_naught)
    Thetas = []
    ThetaC = 0
    flag = 0
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
        if flag == 0:
            if len(Thetas) > 4*NumOfVars:
                if getMaxDiff(Thetas[-4*NumOfVars:]) < 5*a:
                    ThetaC = Thetas[-1]
                    flag = 1
                    CauchyIterations = len(Thetas)
    print str(NumOfVars) + " Vars Test" + str(testno)
    print "ThetaCauchy:", ThetaC, "in", CauchyIterations
    print "ThetaFinal:", Thetas[-1]
    print "ThetaTrue:", coefs[0]
    print ""
##    fig = plt.figure()
##    plt.plot(range(iterations), Thetas)
##    #plt.plot(range(iterations), t1s)
##    print coefs
##    DTnow = datetime.datetime.now()
####    printstr = "y = " + str(Theta[0])
####    for k in range(NumOfVars):
####        printstr = printstr + " + " + str(Theta[k+1]) + "x_" + str(k+1)
####    print printstr
##    figTitle = "GD Var Tests\\" + str(NumOfVars) + str(testno) + ".png"
##    fig.savefig(figTitle)
##    plt.close()
##    model = []
##    for k in range(NumOfVars+1):
##        model = model + [Theta[k]]
##    print model
##    return model


for N in range(9):
    for trialNum in range(10):
        data = createData(N+3)
        GradDescent(data[0], data[1],.01,100,N+3, trialNum)







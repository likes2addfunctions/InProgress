### This is a tool to perform gradient descent on multiple variables.
# Based on Andrew Ng's Machine Learning course at Stanford.
# It currently generates a pseudo random input, then runs the algorithm
# and provides a hypothesis as well as a visualization of convergence.

import random
import numpy
import matplotlib.pyplot as plt
import plotly.plotly as py
	
### Generates data set of [Y, X1, X2, ... Xn], for example [Price, House Size, number of bedrooms, ...]#SampleSize = 50
NumOfVars = 8

Data = []

coefs = []
for i in range(NumOfVars):
    m = 2*random.random() - 1
    coefs = coefs + [m]
        
for i in range(100):
    point = []
    y = 0
    for k in range(NumOfVars):
        x = random.random()
        y = y + coefs[k]*x    
        point = point + [x]
    point = [y] + point
    Data = Data + [point]
    
#print XVect
#print YVect    

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
    print coefs
    printstr = "y = " + str(Theta[0])
    for k in range(NumOfVars):
        printstr = printstr + " + " + str(Theta[k+1]) + "x_" + str(k+1)
    print printstr
    plt.show()


GradDescent(Theta_naught,Data,.01,1000)
#
#plt.scatter(XVect,YVect)
#plt.show()






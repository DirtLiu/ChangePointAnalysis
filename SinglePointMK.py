# coding: utf-8
'''
    Estimate single change point in a sequence with MK method. 
'''

import math
import sys

def getFileData(fileName):
    fieldNames = []
    fieldValues = []
    with open(fileName) as fo:   
        fieldNames = fo.readline().strip('\n').split()
        for line in fo:
            fieldValues.append( line.strip('\n').split() )            
    return fieldNames, fieldValues
      
def calOrderStatistic(xList):      
    orderStatsSequence = []
    for l in range(2, samplesLength + 1):
        orderStatsValue = 0
        for j in range(1, l):
            for i in range(0, j):
                orderStatsValue += (1 if xList[i] <= xList[j] else 0)
        orderStatsSequence.append(orderStatsValue)
    return orderStatsSequence

def calStatisticSequence(OrderStatsSequence):
    statsSequence = [0]
    for i in range(0, samplesLength - 1):        
        E = (i + 2) * (i + 1) / 4.0
        VAR = (i + 2) * (i + 1) * (2.0 * i + 9) / 72.0
        statsValue = (OrderStatsSequence[i] - E) / math.sqrt(VAR)
        statsSequence.append(statsValue)
    return statsSequence 
      
def getMinDistance(x1,x2):
    distance = []
    for i in range(0, samplesLength):
        distance.append( abs(x1[i] - x2[i]) )
    print "distance=", distance
    minDis = min(distance)
    pointIndex = distance.index(minDis)
    pointValue = (x1[pointIndex] + x2[pointIndex]) / 2.0
    return pointValue, pointIndex

if __name__ == "__main__":
    fieldNames, fieldValues = getFileData(raw_input("Input name or address of your data: "))
    inValueName = raw_input("Input the name of field to be processed: ")
    inIDName = raw_input("Input the field name to identify data value: ")

    if (inValueName in fieldNames) and (inIDName in fieldNames):
        fieldValueIndex = fieldNames.index(inValueName)
        fieldIDIndex = fieldNames.index(inIDName)
    else:
        raise ValueError("Can't find out the name in data. Please check in your input name!")
    samples = []
    samplesID =[]
    for fieldValue in fieldValues:
        samples.append( float(fieldValue[fieldValueIndex]) )
        samplesID.append(fieldValue[fieldIDIndex])
        
    global samplesLength
    samplesLength = len(samples)

    originalDl = calOrderStatistic(samples)
    originalUdl =calStatisticSequence(originalDl)
    
    reverseSamples = list(reversed(samples))
    reverseDl = calOrderStatistic(reverseSamples)
    minusUdl = [-i for i in calStatisticSequence(reverseDl)]
    reverseUdl = list( reversed(minusUdl) )
    
    print "originalUdl=", originalUdl
    print "reverseUdl=", reverseUdl
    
    PointValue, pointIndex = getMinDistance(originalUdl, reverseUdl)
    if PointValue < 1.96:
        changePoint = samples[pointIndex]
        changePointID = samplesID[pointIndex]        
        print  'The change point location is: %s, and the value is: %.2f'  %(changePointID, changePoint)
    else:
        print "Oops, there not exist change point in this sequence!"

     





                  
                  
            
            
            
            

            
































    

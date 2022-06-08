from os import path
from array import *
from copy import deepcopy
import numpy as np
import sys
import csv
import time


# Global variables
colNum = 0  # Number of columns, total number of column features, value to be accessed for featureSearch function.
# The rows and columns for the dataset, used in featureSearch, cross validation, and for distance calculation (nearest neighbors distance)
row = []
columnFeature = []

# f=open("mydata.txt","w+")
# sys.stdout=f

def forwardSearch(colNum, row, columnFeature):
    print("Forward Selection is running.")
    start = time.clock()
    currentFeatureSet, accuracyArr, featureOutput = [], [], []
    for i in range(1, colNum):
        print("On the level " + str(i) + " of the search tree")
        featureToAddAtLevel, bestAcc = 0, 0
        for k in range(1, colNum):
            initCopy = deepcopy(currentFeatureSet)  # https://www.geeksforgeeks.org/copy-python-deep-copy-shallow-copy/
            if k not in currentFeatureSet:
                initCopy.append(k)
                print("Adding the feature " + str(k) + ". New features set is: " + str(initCopy))
                acc = leaveOneOutCross(initCopy, row, columnFeature)
                print("Accuracy: " + str(acc))
                if acc > bestAcc:
                    bestAcc = acc
                    featureToAddAtLevel = k
        currentFeatureSet.append(featureToAddAtLevel)
        accuracyArr.append(bestAcc)
        resultCopy = deepcopy(currentFeatureSet)  # output the best features based on best accuracy.
        featureOutput.append(resultCopy)
        print("Feature set " + str(resultCopy) + " was best on the level " + str(i) + ", accuracy is " + str(bestAcc) + "\n")
    # https://www.w3schools.com/python/ref_list_index.asp to find the indexes that created the best accuracy
    end = time.clock()
    print("Finished! The best features subset is " + str(featureOutput[accuracyArr.index(max(accuracyArr))]) + ", its accuracy is " + str(max(accuracyArr) * 100) + "%")
    print ("Time is "+str(end-start)+"s")


def backwardSearch(colNum, row, columnFeature):
    print("Backward Elimination is running.")
    start = time.clock()
    currentFeatureSet = np.arange(1, colNum,1)  # https://realpython.com/how-to-use-numpy-arange/ create a currentFeatureSet withe every feature
    accuracyArr, featureOutput = [], []
    for i in range(1, colNum):
        print("On the level " + str(i) + " of the search tree")
        featureToAddAtLevel, bestAcc = 0, 0
        for k in range(1, colNum):
            initCopy = deepcopy(currentFeatureSet)  # https://www.geeksforgeeks.org/copy-python-deep-copy-shallow-copy/
            if k in currentFeatureSet:
                initCopy = initCopy[initCopy != k]
                print("Removing the feature " + str(k) + ". New features set is: " + str(initCopy))
                acc = leaveOneOutCross(initCopy, row, columnFeature)
                print("Accuracy: " + str(acc))
                if acc > bestAcc:
                    bestAcc = acc
                    featureToAddAtLevel = k

        currentFeatureSet = currentFeatureSet[currentFeatureSet != featureToAddAtLevel]
        accuracyArr.append(bestAcc)
        resultCopy = deepcopy(currentFeatureSet)  # output the best features based on best accuracy.
        featureOutput.append(resultCopy)
        print("Feature set " + str(resultCopy) + " was best on the level " + str(i) + ", accuracy is " + str(bestAcc) + "\n")
    end = time.clock()
    print("Finished! The best features subset is " + str(featureOutput[accuracyArr.index(max(accuracyArr))]) + ", its accuracy is " + str(max(accuracyArr) * 100) + "%")
    print ("Time is "+str(end-start)+"s")


def leaveOneOutCross(initCopy, row, columnFeature):
    count = 0  #help calculate accuracy
    for i in range(len(row)):
        nearestNeighborDistance = nearestNeighborLocation = sys.maxsize  # https://www.geeksforgeeks.org/sys-maxsize-in-python/
        for j in range(len(row)):
            if not i == j:
                distance = 0.0
                for t in range(len(initCopy)):
                    distance += (float(columnFeature[initCopy[t] - 1][i]) - float(columnFeature[initCopy[t] - 1][j])) ** 2
                if distance < nearestNeighborDistance:
                    nearestNeighborDistance = distance
                    nearestNeighborLocation = j
        if row[i] == row[nearestNeighborLocation]:
            count += 1
    return count / len(row)


def main():
    global colNum
    global row
    global columnFeature
    userInput = ""  # The user will be inputting 1, or 2, depending on their algorithm choice
    print("Welcome to Likun Ni's Feature Selection Algorithm." )
    fileInput = input("Type in the name of the file to test:")
    # https://docs.python.org/3/library/os.path.html, using Python OS.path library to check if a file exists
    while not path.exists(fileInput):
        fileInput = input("This file doesn't exit.\nType the name of the file to test:")
    # w3schools.com/python/python_file_open.asp Referenced for opening the file
    # https://docs.python.org/3/library/csv.html
    colNum = len(next(csv.reader(open(fileInput, 'r'), delimiter=' ', skipinitialspace=True)))  # https://www.w3schools.com/python/ref_func_next.asp
    readline = open(fileInput, 'r').readlines()  # https://www.w3schools.com/python/ref_file_readlines.asp
    row = [i.split()[0] for i in readline] # Splitting every single element in the dataset and then appending each indvidual element
    print("Input file:" + fileInput + " successfully\n")
    print("This dataset has " + str(colNum - 1) + " features (not including the class attribute, with " + str(
        len(row)) + " instances.")
    accuracyInit = leaveOneOutCross([], row, columnFeature)
    print("Running nearest neighbor with all " + str(
        colNum - 1) + " features, using \"leave one out\" evaluation, accuracy is " + str(accuracyInit * 100) + "%.\n")
    columnFeature = [[j.split()[i] for j in readline] for i in range(1, colNum)]
    while userInput != '1' and userInput != '2':  # User is asked to choose either 1 or 2 as correct inputs, for one of the two provided algorithms.
        print("Type the number of the algorithm you want to run.")
        print("(1) Forward Selection.       (2) Backward Elimination")
        userInput = input()
        if userInput == '1':
            forwardSearch(colNum, row, columnFeature)
        elif userInput == '2':
            backwardSearch(colNum, row, columnFeature)
        else:
            print("Input incorrect.")

main()

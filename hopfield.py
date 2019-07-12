from PIL import Image
from random import *
import numpy as np
import logfileCreateror as text
import os
import sys
import copy
import time

filepathPics = r"pics\Pics15x15\\"
filepathNoisyPics = r"PicsRausch\noisyPics15x15\\"
convergenceCriteria = 1500


def main(controller):
    start = time.time()
    text.clearLogFile()
    text.log("Starting Module: " + str(sys._getframe().f_code.co_name))
    # learning the pictures
    learningTimeStart = time.time()
    qVectors = createQVectors()
    weightMatrix = calculateWeights(qVectors, controller)
    # safeHopfieldNet(weightMatrix)
    getSafedHopfieldNet()
    learningTimeEnd = time.time()
    text.log("Learning all given Images took: " + str(learningTimeEnd - learningTimeStart) + " seconds")
    controller.changeLearningTimeLabel(learningTimeEnd - learningTimeStart)
    counter = 1

    # each nosy Image in the directory
    for file in os.listdir(filepathNoisyPics):
        filename = os.fsdecode(file)
        if filename.endswith(".png"):
            startExample = time.time()
            controller.changeLeftImage(filepathNoisyPics + filename, counter)
            filepath = str(filepathNoisyPics) + str(filename)
            imgNoisy = Image.open(filepath)
            # imgNoisy = Image.new('RGB', (10, 10), color=(255,255,255))
            xMap = createBinarPixelMap(imgNoisy)
            text.log("das RauschBild \"" + str(filename) + " \" als xMap: " + str(xMap))
            xMap = patternRecognition(xMap, weightMatrix, controller)
            text.log("XMAPneu: " + str(xMap))
            createPixelImage(xMap, filename)
            endExample = time.time()
            text.log("Time needed for Example: " + str(filename) + " timeneeded:" + str(endExample - startExample))
            controller.changeTimeNeededForExampleLabel(endExample - startExample)
            time.sleep(3)

            counter += 1

    end = time.time()
    print("Total time needed: " + str(end - start) + " seconds")
    controller.changeTotalTimeNeededLabel(end - start)


def patternRecognition(xMap, weightMatrix, controller):
    '''in this module we change the Pixxels/Neurons(xMap) in dependency of the learned weights,
     @xMap: are the Neurons of the noisy Picture
     @weightMatrix: is the Matrix with the learned Weights

    :return: the Xmap with the Neurons which are changed based on the weights
     '''
    text.log("Starting Module: " + str(sys._getframe().f_code.co_name))
    count = 0
    noChangesCounter = 0
    xMapOld = copy.deepcopy(xMap)
    neuronNumber = xMap.size
    while (True):
        i = randint(0, neuronNumber - 1)
        weightSum = 0
        for j in range(neuronNumber):
            if i is j:
                continue
            weightSum += weightMatrix[i][j] * xMap[j]

        # tool.log("weightSum: "+ str(weightSum))
        if weightSum < 0:
            xMap[i] = -1
        else:
            xMap[i] = 1

        # text.log("Durchlauf: "+str(count)+ " XMAPneu: " + str(xMap))
        count += 1
        if checkConvergence(xMap, xMapOld):
            noChangesCounter += 1
            if noChangesCounter > convergenceCriteria:
                text.log("Kovergenz gefunden bei Durchlauf: " + str(count - convergenceCriteria))
                break
        else:
            # some Change happened
            tmpImg = createPixelImage(xMap, saveImage=False)
            controller.changeRightImage(tmpImg, count)

            time.sleep(0.01)
            noChangesCounter = 0
            xMapOld = copy.deepcopy(xMap)

    text.log("Das ist die resultierende xMap:\n" + str(xMap))

    return xMap


def createQVectors():
    '''

    In this module we go through all available Pictures in the given Filepath
    and create for each Picture one Q-Vector and add them to a List/Matrix
    Here the AI learns the given Images.

    :return: List of all Q-Vectors
    '''
    text.log("Starting Module: " + str(sys._getframe().f_code.co_name))
    qVectors = np.array([[]])
    qVectorsNum = 1
    for file in os.listdir(filepathPics):
        filename = os.fsdecode(file)
        if filename.endswith(".png"):
            filepath = str(filepathPics) + str(filename)
            imgExample = Image.open(filepath)

            qVector = createBinarPixelMap(imgExample)
            dimensions = qVector.size

            qVectors = np.append(qVectors, [qVector])
            qVectors = qVectors.reshape(qVectorsNum, dimensions)
            qVectorsNum += 1
            continue
        else:
            continue
    # text.log("The qVector List: " + str(qVectors))
    text.log("the qVecotrs are ready")

    return qVectors


def createBinarPixelMap(img):
    '''Befüllung des q Vektors mit 1 und -1;
     Seite 271 im Buch von Ertel'''
    text.log("Starting Module: " + str(sys._getframe().f_code.co_name))
    text.log("Starting to create the Q Vector for given Image")
    pixels = img.load()  # create the pixel map
    pixelVec = np.array([])
    for i in range(img.size[0]):  # for every col:
        for j in range(img.size[1]):  # For every row
            # pixels[i,j] = (250, 250, 250) # set the colour accordingly
            if pixels[i, j] == (255, 255, 255):
                # weißer Pixel
                pixelVec = np.append(pixelVec, [1])
                # print(str(pixels[i, j]) + " Row:"+str(j)+" Col:"+str(i))
            else:
                # schwarzer Pixel
                pixelVec = np.append(pixelVec, [-1])

    return pixelVec


def calculateWeights(qVectors, controller):
    '''calculates the Weights for the Neurons with the given Q-Vectors
    Seite 272 im Buch von Ertel 9.1'''
    text.log("Starting Module: " + str(sys._getframe().f_code.co_name))
    text.log("Starting to calculaate the Weight Matrix for given Image")
    schritteProZeit = 40000 * 0.08
    count = 0
    weightValue = 0
    qVectorsNum = np.size(qVectors, 0)
    dimensions = np.size(qVectors, 1)
    weightCounter = 0
    weightMatrix = np.array([[]])
    tmpVec = np.array([])

    text.log("Number of Q-Vectors: " + str(qVectorsNum))
    controller.changeLearnedExamplesLabel(qVectorsNum)
    text.log("Number of dimensions: " + str(dimensions))
    calculatedSteps = dimensions * dimensions * qVectorsNum
    progressbarOnePrecent = calculatedSteps / 100
    text.log("Anzahl der Rechenschritte: " + str(calculatedSteps))
    # rechenZeitsekunden = (calculatedSteps/40000)*0.08
    # text.log("Predicted Time Needed: "+str(rechenZeitsekunden)+"s  "+str(rechenZeitsekunden/60) + "min  "+str(rechenZeitsekunden/3600)+ " h")
    iterationStart = time.time()
    progessLearning = 1
    detailTimerStart = time.time()
    stepsCounter = 0


    for i in range(dimensions):

        for j in range(dimensions):

            weightCounter += 1
            for N in range(qVectorsNum):
                stepsCounter += 1
                if i is j:
                    count += 1
                    weightValue += 0
                    continue
                else:
                    weightValue += (qVectors[N][j] * qVectors[N][i])

                if stepsCounter >= progressbarOnePrecent * progessLearning:
                    detailTimerEnd = time.time()
                    controller.changeProgressbar(progessLearning)
                    text.log("process: " + str(progessLearning) + "% at step: "+str(stepsCounter)+" out of "+str(calculatedSteps)+ "   Time needed: " + str(
                        detailTimerEnd - detailTimerStart) + "s")
                    detailTimerStart = time.time()
                    progessLearning += 1

            weightValue = weightValue / dimensions
            tmpVec = np.append(tmpVec, [weightValue])
            weightValue = 0

        weightMatrix = np.append(weightMatrix, [tmpVec])
        weightMatrix = weightMatrix.reshape(i + 1, dimensions)
        tmpVec = np.array([])

    iterationEnd = time.time()
    # text.log("CalculateWeights, eigentliche Rechenschritte: "+ str(iterationCounter))
    text.log("Calculateweights, Rechenzeit für die Iterattion: " + str(iterationEnd - iterationStart) + "s")
    # text.log("The Weight Matrix: " + str(weightMatrix))
    text.log("The number of the values in the Weight Matrix " + str(weightCounter))
    text.log(" The Weight Matrix has " + str(dimensions) + " Dimensions")
    return weightMatrix

    # print(weightCounter)


def createPixelImage(pixelMap, fileName=None, saveImage=True):
    '''
    Here we will create an Image by the given pixelMap, we will save as AI-Art
    :param pixelMap: The Values for the Pixels
    :param fileName: Name of the Image for saving
    :param saveImage: if False it won't save the Image, it will return the Image-Object

    '''

    imageDefinition = np.sqrt(pixelMap.size)
    imageDefinition = int(imageDefinition)
    img = Image.new('RGB', (imageDefinition, imageDefinition), color=(255, 255, 255))
    pixels = img.load()
    breiteHöhe = img.size[0]
    for i in range(img.size[0]):  # for every col:
        for j in range(img.size[1]):  # For every row
            # print("j: "+ str(j)+ " i: "+str(i)+" pixelMap[i+j]: "+str(pixelMap[i+j*10]))
            # pixels[i,j] = (250, 250, 250) # set the colour accordingly
            if pixelMap[i * breiteHöhe + j] == 1:
                img.putpixel((i, j), (255, 255, 255))
            elif pixelMap[i * breiteHöhe + j] == -1:
                img.putpixel((i, j), (0, 0, 0))
            else:
                print("ERROR")
                exit(1)
    if not saveImage:
        return img
    else:
        img.save(r'AI-Art\AI-' + str(fileName) + '.png')


def checkConvergence(xMapNew, xMapOld):
    '''
    Checks if the Hopfield-Net did converged or not
    :param xMapNew: The new Xmap
    :param xMapOld: the old one
    :return: True when converged, False if not
    '''
    epsilon = 1
    differences = 0
    for i in range(xMapNew.size):
        if xMapNew[i] != xMapOld[i]:
            differences += 1

    if differences < epsilon:
        return True
    else:
        return False


def safeHopfieldNet(weightMatrix):
    logfile = r"learnedHopfieldNets" + filepathPics[4:-2] + ".log"
    print(logfile)
    # first clear entrance
    with open(logfile, "w") as file:
        pass

    # print(weightMatrix)
    file = open(logfile, "a")

    for i in weightMatrix:
        file.write(str(i))

    file.close()


def getSafedHopfieldNet():
    logfile = r"learnedHopfieldNets\Pics15x15.log"
    weightMatrix = np.array([[]])
    tmpVec = np.array([])
    file = open(logfile, "r")

    op = file.read()
    i = 0

    while True:
        print(op[i])
        i += 1

        if op[i] == ']':
            break

        # if op[i] == '[':
        # i +=1
        # while True:
        #   if
        # tmpVec = np.append(op)


if __name__ == "__main__":
    main()

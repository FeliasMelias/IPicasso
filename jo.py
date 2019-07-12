import numpy as np
import io

k = 100245


def getSafedHopfieldNet():
    logfile = r"learnedHopfieldNets\Pics15x15.log"
    weightMatrix = np.array([[]])
    tmpVec = np.array([])
    file = open(logfile, "r")

    op = file.read()
    i = 0
    stringNumb = ""
    while True:

        #print(op[i])
        if op[i] == '[':

            i+=2
            while op[i] != ' ':
                stringNumb += op[i]
                i+=1
            print(float(stringNumb))
            tmpVec = tmpVec.appe




        if op[i] == ']':
            break
        i += 1



def justTheHalfMatrix():
    myArray = []
    for i in range(10):
        myArray.append(i)
        for j in range(10):
            myArray.append(j)


    print(myArray)
justTheHalfMatrix()

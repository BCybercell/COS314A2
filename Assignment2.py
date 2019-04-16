import time
import math
import copy
import json  # TODO remove after testing


def readFile(aName):
    data = []
    f = open(aName, "r")
    for x in f:
        data.append(x)
    f.close()
    return data


def createDict(aData):
    lDict = {
        'Line': []
    }
    for line in aData:  # TODO find better name for line
        lineDict = {
            'Value': True,
            'Data': {}
        }

        cleanLine = line.rstrip("\n")  # Removes end-line character from line
        cleanLine = cleanLine.strip()  # Removes whitespaces
        cleanLine = cleanLine.split()  # converts string to array of size 2 (data and value)

        # dataOrValue checks if it is a True/False or 0 or 1
        for dataOrValue in cleanLine:  # TODO find better name for dataOrValue
            if dataOrValue == 'True':
                lineDict['Value'] = True
            elif dataOrValue == 'False':
                lineDict['Value'] = False
            else:  # if 0 or 1
                count = 0
                for data in dataOrValue:
                    if data == '1':  # converts 0 or 1 to True/False
                        lineDict['Data'][count] = True
                    else:
                        lineDict['Data'][count] = False
                    count += 1  # assumed counter necessary for tree creation
        lDict['Line'].append(lineDict)
    return lDict


def calcEntropy(aNumTrue, aNumFalse):
    lTotal = aNumTrue + aNumFalse
    if lTotal == 0:
        return 0

    lDivFalse = aNumFalse / lTotal
    lDivTrue = aNumTrue / lTotal
    if lDivTrue == 0:
        return - (lDivFalse * math.log(lDivFalse, 2))
    elif lDivFalse == 0:
        return -lDivTrue * math.log(lDivTrue, 2)
    else:
        lSetEntropy = -lDivTrue * math.log(lDivTrue, 2) - (
                lDivFalse * math.log(lDivFalse, 2))
    return lSetEntropy


def computeSetEntropy(aDict):
    lSetTrue = 0
    lSetFalse = 0
    lTotal = 0
    # lSetEntropy = 0
    for line in aDict['Line']:
        if line['Value']:
            lSetTrue += 1
        else:
            lSetFalse += 1
        lTotal += 1
    lSetEntropy = -(lSetTrue / lTotal) * math.log((lSetTrue / lTotal), 2) - (
            (lSetFalse / lTotal) * math.log((lSetFalse / lTotal), 2))
    return lSetTrue, lSetFalse, lSetEntropy

node = {
        'Label': -1,
        'True': {},
        'False': {},
        'EndOutcome':
        {
            'True': 0,
            'False': 0
        },
        'Entropy':
        {
            'True': 0,
            'False': 0,
            'Value' : 0
        }

    }


def buildTreeTest(aNode, aArr, aDict):  # arr is a sorted ordering of splitting
    lArr = aArr
    num = lArr.pop(0)

    if not aNode:  # if the doesn't node exists
        aNode = copy.deepcopy(node)
        aNode['Label'] = num

    if aDict['Value']:
        aNode['Entropy']['True'] = aNode['Entropy']['True'] + 1
    else:
        aNode['Entropy']['False'] = aNode['Entropy']['False'] + 1

    if lArr:  # If we need to go deeper in the tree

        aNode['Entropy']['Value'] = calcEntropy(aNode['Entropy']['True'], aNode['Entropy']['False'])

        if aDict['Data'][aNode['Label']]:
            tempNode = buildTreeTest(aNode['True'], lArr, aDict)
            aNode['True'] = tempNode
        else:
            tempNode = buildTreeTest(aNode['False'], lArr, aDict)
            aNode['False'] = tempNode
    else:  # if we reached the leaf
        if aDict['Value']:
            aNode['EndOutcome']['True'] = aNode['EndOutcome']['True'] + 1
        else:
            aNode['EndOutcome']['False'] = aNode['EndOutcome']['False'] + 1
    return aNode


def evaluateTree(aNode, aDict):  # TODO fix with newNode structure
    if aDict['Data'][aNode['Label']]:
        if aNode['True']:
            return evaluateTree(aNode['True'], aDict)
        else:
            if aNode['EndOutcome']['True'] > aNode['EndOutcome']['False']:
                return True
            else:
                return False
    else:
        if aNode['False']:
            return evaluateTree(aNode['False'], aDict)
        else:
            if aNode['EndOutcome']['True'] > aNode['EndOutcome']['False']:
                return True
            else:
                return False


def jsonFile(aDictionary, aFileName):  # TODO remove after testing
    with open(aFileName, 'w') as j:
        json.dump(aDictionary, j)


def testCode():
    start = time.time()
    lData = readFile('Mini_Understanding.txt')
    # Mini_Understanding
    # Training_Data
    print('Data received')
    lDictData = createDict(lData)
    print('Dictionary created')

    setTrue, setFalse, setEntropy = computeSetEntropy(lDictData)
    print('True values:', setTrue)
    print('False values:', setFalse)
    print('Entropy:', setEntropy)
    end = time.time()
    print('time elapsed:', end - start)
    print('===================================================================')

    print('Building tree')
    ar = []
    for x in range(5):
    # for x in range(100):
        ar.append(x)

    root = {}
    count = 0
    for line in lDictData['Line']:
        root = buildTreeTest(root, ar.copy(), line)
        # count += 1
        # print('line :', count)
    print('Tree built')
    end = time.time()
    print('time elapsed:', end - start)
    print('===================================================================')

    # print('Saving temp file')
    # jsonFile(root, 'rootTest.json')
    # print('Temp file saved')

    print('testing tree')
    tru = 0
    count = 0
    # =====================================================

    # # lData = readFile('Test_Data.txt')
    # lData = readFile('Validation_Data.txt')
    # print('Data received')
    # lDictDataTest = createDict(lData)
    # print('Dictionary created')

    # ===========================================
    # for line in lDictDataTest['Line']:
    for line in lDictData['Line']:

        test = evaluateTree(root, line)
        if line['Value'] == test:
            tru += 1
        count += 1
    print('Accuracy', (tru/count)*100, '%')
    # print(test)
    end = time.time()
    print('time elapsed:', end - start)


testCode()

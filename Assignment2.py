import time
import math
import copy
import json  # TODO remove after testing
import random


gDictDataTraining = {}


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
            'Value': 0
        },
    'Gain': -1,
    'List': []

}


def buildTreeTest(aNode, aArr, aDict):  # arr is a sorted ordering of splitting
    lArr = aArr
    num = lArr.pop(0)

    if not aNode:  # if the doesn't node exists
        # aNode = node.copy()
        aNode = copy.deepcopy(node)
        aNode['Label'] = num

    if aDict['Value']:
        aNode['Entropy']['True'] = aNode['Entropy']['True'] + 1
    else:
        aNode['Entropy']['False'] = aNode['Entropy']['False'] + 1
    aNode['Entropy']['Value'] = calcEntropy(aNode['Entropy']['True'], aNode['Entropy']['False'])

    if lArr:  # If we need to go deeper in the tree
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
    lData = readFile('Training_Data.txt')
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
    # for x in range(5):
    for x in range(100):
        ar.append(x)

    root = {}
    for line in lDictData['Line']:
        root = buildTreeTest(root, ar.copy(), line)
        # count += 1
        # print('line :', count)
    print('Tree built')
    end = time.time()
    print('time elapsed:', end - start)
    print('===================================================================')

    print('Adding validation data')
    lData = readFile('Validation_Data.txt')
    print('Data received')
    lDictData = createDict(lData)
    print('Dictionary created')

    print('Building tree')
    for line in lDictData['Line']:
        root = buildTreeTest(root, ar.copy(), line)
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

    # lData = readFile('Test_Data.txt')
    # # lData = readFile('Validation_Data.txt')
    # print('Data received')
    # lDictDataTest = createDict(lData)
    # print('Dictionary created')

    # ===========================================
    # for line in lDictDataTest['Line']:

    print('Accuracy with no GA', (tru / count) * 100, '%')
    # print(test)
    end = time.time()
    print('time elapsed:', end - start)


def calEffectiveness(root, aDictData):
    tru = 0
    count = 0
    for line in aDictData:
        test = evaluateTree(root, line)
        if line['Value'] == test:
            tru += 1
        count += 1
    return tru/count


def confusionData(root, aDictData):
    lTruePositive = 0
    lTrueNegative = 0
    lFalsePositive = 0
    lFalseNegative = 0
    for line in aDictData:
        test = evaluateTree(root, line)
        if test:
            if line['Value']:
                lTruePositive += 1
            else:
                lFalsePositive += 1
        else:
            if line['Value']:
                lFalseNegative += 1
            else:
                lTrueNegative += 1

    return lTruePositive, lTrueNegative, lFalsePositive, lFalseNegative


def createRandomChild(aDictData, randomNum):
    child = {}
    for line in aDictData:
        child = buildTreeTest(child, [randomNum, 100], line)
    if 'False' not in child or 'True' not in child:
        i = 0
    if 'Entropy' in child:
        lTotal = child['Entropy']['True'] + child['Entropy']['False']
    else:
        # print('line', child)
        lTotal = 1
    if 'Entropy' in child['False'] and 'Entropy' in child['True']:
        child['Gain'] = child['Entropy']['Value'] - (
            (child['Entropy']['True'] / lTotal) * child['True']['Entropy']['Value']) - (
            (child['Entropy']['False'] / lTotal) * child['False']['Entropy']['Value'])
    elif 'Entropy' in child['False']:
        child['Gain'] = child['Entropy']['Value'] - (
                (child['Entropy']['False'] / lTotal) * child['False']['Entropy']['Value'])
    else:
        child['Gain'] = child['Entropy']['Value'] - (
                (child['Entropy']['True'] / lTotal) * child['True']['Entropy']['Value'])
        # print('line', child)

    child['False'] = {}
    child['True'] = {}
    return child


def sortByGain(val):
    return val['Node']['Gain']


def sortByGain2(val):
    return val['Gain']


def sortByEffectiveness(val):
    return val['Effectiveness']


def removeChildren(aChildren, aStrength):
    numToRemove = int(len(aChildren)*aStrength)
    for x in range(numToRemove):
        aChildren.pop()
    return aChildren


def filterDict(aDict, toKeep):
    tempDict = []
    for line in aDict:
        check = 1  # if 0 then one check is false
        for lineToKeep in toKeep:
            if not lineToKeep['Value'] == line['Data'][lineToKeep['Label']]:
                check = 0
        if check == 1:
            tempDict.append(line)
    return tempDict


def buildID3(aList, aDictData, path):
    lArr = copy.deepcopy(aList)
    # num = lArr.pop(0)
    # print('        [+]Filtering Dictionary')
    newDict = filterDict(aDictData, path)
    # print('        [+]Dictionary Filtered')
    candidates = []

    for num in lArr:
        if newDict:
            tempNode = createRandomChild(newDict, num)
        else:
            tempNode = copy.deepcopy(node)
            tempNode['Label'] = num
        candidates.append(tempNode)
    candidates.sort(key=sortByGain2, reverse=True)
    selectedChild = candidates[0]
    num = lArr.pop(lArr.index(selectedChild['Label']))

    pathTrue = path.copy()
    pathFalse = path.copy()
    # if there is a path to follow and it is needed (confusion between true and false exist)
    if lArr and selectedChild['Entropy']['True'] > 0 and selectedChild['Entropy']['False'] > 0:
        pathTrue.append({
             'Label': num,
             'Value': True})
        pathFalse.append({
            'Label': num,
            'Value': False})
        tempNode = buildID3(lArr, newDict, pathTrue)
        selectedChild['True'] = tempNode

        tempNode = buildID3(lArr, newDict, pathFalse)
        selectedChild['False'] = tempNode

    else:
        # if lArr:
        #     print('Yata')
        selectedChild['EndOutcome']['True'] = selectedChild['Entropy']['True']
        selectedChild['EndOutcome']['False'] = selectedChild['Entropy']['False']

    return selectedChild


def mate(aParent1, aParent2):
    global gDictDataTraining
    # Combine two arrays/lists
    lList = aParent1['NodeArr']
    lListC = copy.deepcopy(lList)
    lTempList = aParent2['NodeArr']
    for item in lTempList:
        if item not in lListC:
            lListC.append(item)

    if not set(lListC) == set(lList):
        print('     [+]Building Tree')
        root = buildID3(lListC.copy(), copy.deepcopy(gDictDataTraining), [])
        print('     [+]Tree Built')
    else:
        print('     [+]No building of tree required')
        return aParent1
    child = {
        'Node': root,
        'NodeArr': lListC,  # here maybe
        'Effectiveness': calEffectiveness(root, gDictDataTraining)
    }
    return child


def Evolve(children):

    print('[+]Removing weak children')
    children = removeChildren(children, 0.67)  # removes lower 75 children
    print('[+]Weak children removed')
    print('[+]Mating and mutating children')
    cnt = 1
    length = len(children)
    for x in range(length):
        child = children[x]
        print(' [*]Child:', cnt, 'of', length)
        begin = time.time()
        cnt += 1
        randomNum = random.randint(1, length+1)
        if randomNum >= length:
            randomNum = length-1
        print('   [+]Mating children', cnt-1, 'and', randomNum)
        children.append(mate(child, children[randomNum]))  # creates 400 children
        # if randomNum > lent/4:
        mutation = random.randint(1, 101) - 1  # TODO switch to 101
        if mutation >= 100:  # TODO switch to 100
            mutation = 99   # TODO switch to 99
        mutatedChild = {
            'NodeArr': [mutation]
        }
        print('   [+]Mutating child with:', mutation)
        children.append(mate(child, mutatedChild))
        endTime = time.time()
        print(' [*]Child took', endTime-begin, 's')
    print('[+]Children mated and mutated')

    return children


def GA():
    global gDictDataTraining
    children = []
    print('[+]Creating random children')
    for x in range(21):
        randomNum = random.randint(1, 101)-1  # TODO switch to 101
        if randomNum >= 100:  # TODO switch to 100
            randomNum = 99  # TODO switch to 99
        #  create children randomly
        tempNode = createRandomChild(gDictDataTraining, randomNum)
        child = {
            'Node': tempNode,
            'NodeArr': [tempNode['Label']],
            'Effectiveness': -1
        }
        children.append(child)
    print('[+]Random children created')
    children.sort(key=sortByGain, reverse=True)
    topEff = 0.0
    x = 0
    while topEff < 0.999999:  # Basically 100% accuracy (99.9999%)
        x += 1
        print('')
        print('')
        print('============================================================================================')
        print('============================================================================================')
        print('============================================================================================')
        print('[*]Mutation :', x)
        children = Evolve(children)

        children.sort(key=sortByEffectiveness, reverse=True)
        topEff = children[0]['Effectiveness']
        print('[*]Top effectiveness :', topEff)
        print('[*]Top attributes :', children[0]['NodeArr'])
    lData = readFile('Validation_Data.txt')
    # Mini_Understanding
    # Training_Data
    print('[+]Data received')
    lDictData = createDict(lData)
    lDictData = lDictData['Line']

    topEff = 0.0
    x = 0
    for child in children:
        child['Effectiveness'] = calEffectiveness(child['Node'], lDictData)
    # this keeps evolving till either it reaches 100% accuracy or 120 generations have been run,
    # but it still needs to get at least 86% accuracy.
    while topEff < 0.9999 and (x < 120 or x < 0.86):  # changed to 99.99% from 85
        x += 1
        print('')
        print('')
        print('============================================================================================')
        print('============================================================================================')
        print('============================================================================================')
        print('[*]Mutation 2.0 :', x)
        children = Evolve(children)
        for child in children:
            child['Effectiveness'] = calEffectiveness(child['Node'], lDictData)
        children.sort(key=sortByEffectiveness, reverse=True)
        topEff = children[0]['Effectiveness']
        print('[*]Top effectiveness :', topEff)
        print('[*]Top attributes :', children[0]['NodeArr'])
        print('[*]Number of attributes :', len(children[0]['NodeArr']))
    print('')
    print('')
    print('============================================================================================')
    print('============================================================================================')
    print('============================================================================================')
    return children[0]


def testCodeGA():
    global gDictDataTraining
    start = time.time()
    lData = readFile('Training_Data.txt')
    # Mini_Understanding
    # Training_Data
    print('[+]Data received')
    gDictDataTraining = createDict(lData)
    gDictDataTraining = gDictDataTraining['Line']
    print('[+]Dictionary created')
    print('==================================================')
    #
    print('[+]Calling GA')
    children = GA()
    lData = readFile('Test_Data.txt')
    # lData = readFile('Validation_Data.txt')
    print('[+]Data received')
    lDictDataTest = createDict(lData)
    print('[+]Dictionary created')
    setTrue, setFalse, setEntropy = computeSetEntropy(lDictDataTest)
    print('[*]True values:', setTrue)
    print('[*]False values:', setFalse)
    print('[*]Entropy:', setEntropy)
    eff = calEffectiveness(children['Node'], lDictDataTest['Line'])
    print('[*]Final Effectiveness:', eff)
    print('==================================================')
    print('==================================================')
    print('==================================================')
    lTruePositive, lTrueNegative, lFalsePositive, lFalseNegative = confusionData(children['Node'], lDictDataTest['Line'])
    print('[*]True positive:', lTruePositive)
    print('[*]True negative:', lTrueNegative)
    print('[*]False positive:', lFalsePositive)
    print('[*]False negative:', lFalseNegative)
    print('==================================================')
    print('==================================================')
    print('==================================================')
    print('[+]Saving temp file')
    jsonFile(children['Node'], 'topChildRougher.json')
    print('[+]Temp file saved')
    end = time.time()
    print('[*]time elapsed:', end - start)


# testCode()
testCodeGA()

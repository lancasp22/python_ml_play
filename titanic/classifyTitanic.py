def getSex(row):
    if row["Sex"] == "male":
        return 0
    else:
        return 1

def getDeparturePort(row):
    if row["Embarked"] == "C":
        return 1
    if row["Embarked"] == "Q":
        return 2
    else:
        return 0

def getCabin(row):
    if row["Cabin"]:
        char = row["Cabin"][0]
        if char > "A" and char <= "G":
            return ord(char)
        else:
            return 0
    else:
        return 0

def getFamilySize(row):
    return row["SibSp"] + row["Parch"]

def formatFeatures(row):
    record = []
    record.append(row["Pclass"])
    record.append(getSex(row))
    # record.append(row["Fare"])
    # record.append(getDeparturePort(row))
    # record.append(row["SibSp"])
    # record.append(row["Parch"])
    # record.append(row["Parch"] + row["SibSp"])
    record.append(getCabin(row))
    # record.append(getFamilySize(row))
    if row["Age"]:
        record.append(row["Age"])
    else:
        record.append(20)
    return record

import csv
with open('data/train.csv') as csvfile:
    trainFeatures = []
    trainLabels = []
    reader = csv.DictReader(csvfile)

    for row in reader:
        trainFeatures.append(formatFeatures(row))
        trainLabels.append(row["Survived"])

csvfile.close()

with open('data/test.csv') as csvfile:
    testFeatures = []
    testIds = []
    reader = csv.DictReader(csvfile)

    for row in reader:
        testFeatures.append(formatFeatures(row))
        testIds.append(row["PassengerId"])

csvfile.close()

from sklearn import tree

trainCount=700

clf = tree.DecisionTreeClassifier(min_samples_split=5)
clf.fit(trainFeatures[0:trainCount], trainLabels[0:trainCount])
print "Decision Tree"
print clf.score(trainFeatures[0:trainCount], trainLabels[0:trainCount])
print clf.score(trainFeatures[trainCount:], trainLabels[trainCount:])

from sklearn.svm import SVC
clf = SVC(kernel="linear")
clf.fit(trainFeatures[0:trainCount], trainLabels[0:trainCount])
print "Linear SVM"
print clf.score(trainFeatures[0:trainCount], trainLabels[0:trainCount])
print clf.score(trainFeatures[trainCount:], trainLabels[trainCount:])

from sklearn.svm import SVC
clf = SVC(kernel="rbf", C=100)
clf.fit(trainFeatures[0:trainCount], trainLabels[0:trainCount])
print "rbf SVM"
print clf.score(trainFeatures[0:trainCount], trainLabels[0:trainCount])
print clf.score(trainFeatures[trainCount:], trainLabels[trainCount:])

from sklearn.naive_bayes import GaussianNB
import numpy as np
clf = GaussianNB()
trainFeatures = np.array(trainFeatures, dtype = 'float_')
clf.fit(trainFeatures[0:trainCount], trainLabels[0:trainCount])
print "Naive Bayes"
print clf.score(trainFeatures[0:trainCount], trainLabels[0:trainCount])
print clf.score(trainFeatures[trainCount:], trainLabels[trainCount:])


from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(random_state=1)
trainFeatures = np.array(trainFeatures, dtype = 'float_')
clf.fit(trainFeatures[0:trainCount], trainLabels[0:trainCount])
print "Random Forest"
print clf.score(trainFeatures[0:trainCount], trainLabels[0:trainCount])
print clf.score(trainFeatures[trainCount:], trainLabels[trainCount:])

# **********FINALLY *************
clf = tree.DecisionTreeClassifier(min_samples_split=5)
trainFeatures = np.array(trainFeatures, dtype = 'float_')
clf.fit(trainFeatures, trainLabels)
print "DT full train"
# print clf.score(trainFeatures, trainLabels)

testFeatures = np.array(testFeatures, dtype = 'float_')
predictions = clf.predict(testFeatures)
#print predictions

with open('data/submission.csv', "wb") as csvfile:
    fieldnames = ['PassengerId', 'Survived']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for idx, item in enumerate(predictions):
        writer.writerow({'PassengerId': testIds[idx], 'Survived': item})

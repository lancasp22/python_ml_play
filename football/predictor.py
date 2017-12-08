import math

def getRankingMargin(result):
    return result['HomeTeamScore'] - result['AwayTeamScore']
    # margin = result['HomeTeamScore'] - result['AwayTeamScore']
    # low_score = min(result['HomeTeamScore'],result['AwayTeamScore'])
    # return margin/math.log(low_score + 3, 3)

def suggestBets(proba):
    # ***** Suggested bets *************
    with open('data/E0_fixtures.csv') as fixturesCsvFile:
        idx = 0
        reader = csv.DictReader(fixturesCsvFile)
        for row in reader:
            home_factor = float(row['BbAvH']) * proba[idx][0]
            draw_factor = float(row['BbAvD']) * proba[idx][1]
            away_factor = float(row['BbAvA']) * proba[idx][2]
            best_bet = 'Home'
            factor = home_factor
            if draw_factor > home_factor and draw_factor > away_factor:
                best_bet = 'Draw'
                factor = draw_factor
            if away_factor > home_factor and away_factor > draw_factor:
                best_bet = 'Away'
                factor = away_factor
            # print 'Home odds {0} Home prob {1}, Draw odds {2} Draw prob {3}, Away odds{4} Away prob {5}'.format(float(row['BbAvH']), proba[idx][0],float(row['BbAvD']), proba[idx][1],float(row['BbAvA']), proba[idx][2])
            # print 'Home factor {0}, Drawfactor {1}, Away factor {2}'.format(home_factor, draw_factor, away_factor)
            print 'The best bet for {0} vs {1} is {2}, factor is {3}'.format(row['HomeTeam'], row['AwayTeam'], best_bet,
                                                                             factor)
            idx = idx + 1

    fixturesCsvFile.close()


import csv
with open('data/teams.csv') as teamsCsvFile:
    teamsDict = {}
    reader = csv.DictReader(teamsCsvFile)

    for row in reader:
        teamsDict[row['Name']] = {'Ranking': float(row['Ranking']), 'HomeRanking': float(row['Ranking']),'AwayRanking': float(row['Ranking']),
                                  'TotalRankingPoints': 0.0, 'TotalGames': 0, 'HomeRankingPoints' : 0.0, 'HomeGames': 0,  'AwayRankingPoints' : 0.0, 'AwayGames': 0 }

teamsCsvFile.close()

with open('data/E0.csv') as resultsCsvFile:
    resultsList = []
    reader = csv.DictReader(resultsCsvFile)

    for row in reader:
        resultsList.append({'HomeTeam': row['HomeTeam'], 'HomeTeamScore': int(row['FTHG']), 'AwayTeam': row['AwayTeam'], 'AwayTeamScore': int(row['FTAG'])})

resultsCsvFile.close()

# print resultsList

for i in range(0, 25):
    for result in resultsList:
        homeTeam = teamsDict[result['HomeTeam']]
        awayTeam = teamsDict[result['AwayTeam']]
        combinedRanking = homeTeam['Ranking'] + awayTeam['Ranking']
        combinedHomeAwayRanking = homeTeam['HomeRanking'] + awayTeam['AwayRanking']
        homeTeamRankingPoints = (combinedRanking + getRankingMargin(result))/2
        homeTeamHomeAwayRankingPoints = (combinedHomeAwayRanking + getRankingMargin(result)) / 2
        awayTeamRankingPoints = (combinedRanking - getRankingMargin(result)) / 2
        awayTeamHomeAwayRankingPoints = (combinedHomeAwayRanking - getRankingMargin(result)) / 2

        homeTeam['TotalGames'] = homeTeam['TotalGames'] + 1
        homeTeam['HomeGames'] = homeTeam['HomeGames'] + 1
        homeTeam['TotalRankingPoints'] = homeTeam['TotalRankingPoints'] + homeTeamRankingPoints
        homeTeam['HomeRankingPoints'] = homeTeam['HomeRankingPoints'] + homeTeamHomeAwayRankingPoints

        awayTeam['TotalGames'] = awayTeam['TotalGames'] + 1
        awayTeam['AwayGames'] = awayTeam['AwayGames'] + 1
        awayTeam['TotalRankingPoints'] = awayTeam['TotalRankingPoints'] + awayTeamRankingPoints
        awayTeam['AwayRankingPoints'] = awayTeam['AwayRankingPoints'] + awayTeamHomeAwayRankingPoints

    # print teamsDict

    for key in teamsDict:
        teamsDict[key]['Ranking'] = teamsDict[key]['TotalRankingPoints']/teamsDict[key]['TotalGames']
        teamsDict[key]['HomeRanking'] = teamsDict[key]['HomeRankingPoints'] / teamsDict[key]['HomeGames']
        teamsDict[key]['AwayRanking'] = teamsDict[key]['AwayRankingPoints'] / teamsDict[key]['AwayGames']
        teamsDict[key]['TotalRankingPoints'] = 0.0
        teamsDict[key]['TotalGames'] = 0
        teamsDict[key]['HomeRankingPoints'] = 0.0
        teamsDict[key]['HomeGames'] = 0
        teamsDict[key]['AwayRankingPoints'] = 0.0
        teamsDict[key]['AwayGames'] = 0

print teamsDict

#***** NB using single ranking *************
testFeatures = []
with open('data/E0_fixtures.csv') as fixturesCsvFile:
    reader = csv.DictReader(fixturesCsvFile)

    for row in reader:
        feature = [teamsDict[row['HomeTeam']]['Ranking'], teamsDict[row['AwayTeam']]['Ranking']]
        testFeatures.append(feature)

fixturesCsvFile.close()
print "Test features for single ranking"
print testFeatures

trainFeatures = []
trainLabels = []
for result in resultsList:
    feature = [teamsDict[result['HomeTeam']]['Ranking'], teamsDict[result['AwayTeam']]['Ranking']]
    trainFeatures.append(feature)
    label = 0
    if result['HomeTeamScore'] == result['AwayTeamScore']:
        label = 1
    if result['HomeTeamScore'] < result['AwayTeamScore']:
        label = 2
    trainLabels.append(label)

from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()
clf.fit(trainFeatures, trainLabels)
print "Score using NB + single ranking"
print clf.score(trainFeatures, trainLabels)

#***** NB using home/away ranking *************
testFeatures = []
with open('data/E0_fixtures.csv') as fixturesCsvFile:
    reader = csv.DictReader(fixturesCsvFile)

    for row in reader:
        feature = [teamsDict[row['HomeTeam']]['HomeRanking'], teamsDict[row['AwayTeam']]['AwayRanking']]
        testFeatures.append(feature)

fixturesCsvFile.close()
print "Test features for Home/Away ranking"
print testFeatures

trainFeatures = []
trainLabels = []
for result in resultsList:
    feature = [teamsDict[result['HomeTeam']]['HomeRanking'], teamsDict[result['AwayTeam']]['AwayRanking']]
    trainFeatures.append(feature)
    label = 0
    if result['HomeTeamScore'] == result['AwayTeamScore']:
        label = 1
    if result['HomeTeamScore'] < result['AwayTeamScore']:
        label = 2
    trainLabels.append(label)

clf = GaussianNB()
clf.fit(trainFeatures, trainLabels)
print "Score using NB + H/A ranking"
print clf.score(trainFeatures, trainLabels)

print "NB features and probabilities"
print clf.predict(testFeatures)
proba = clf.predict_proba(testFeatures)
print proba
suggestBets(proba)

#***** SVM using home/away ranking *************
from sklearn.svm import SVC
clf = SVC(kernel="rbf", C=0.4, probability=True)
clf.fit(trainFeatures, trainLabels)
print "Score using SVC + H/A ranking"
print clf.score(trainFeatures, trainLabels)

print "SVC features and probabilities"
print clf.predict(testFeatures)
proba = clf.predict_proba(testFeatures)
print proba

suggestBets(proba)


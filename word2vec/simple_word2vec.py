from gensim.models import Word2Vec
from sklearn.decomposition import PCA
from matplotlib import pyplot

def getGender(row):
    if row["sex"]:
        if row["sex"] == 'M':
            return 1
        else:
            return 2
    return 0

def getAge(row):
    if row["age"]:
        if row["age"] == 'NULL':
            return 15.0
        else:
            return row["age"]
    return 15.0


def splitOccupation(occupation):
    import re
    words = re.split('\W+', occupation)
    return_words = []
    for word in words:
        if len(word) > 2 and word != 'AND':
            return_words.append(word)
    return return_words

def get_sentence_vector(sentence, model):

    words = splitOccupation(sentence)

    if len(words) < 1:
        return None

    vector =[]

    word_count_found = 0
    for word in words:
        if word in model.wv.vocab:
            word_count_found = word_count_found + 1
            if word_count_found == 1:
                vector = model[word]
            else:
                new_vector = []
                for idx, val in enumerate(vector):
                    new_vector.append(vector[idx] + model[word][idx])
                vector = new_vector

    if word_count_found > 0:
        new_vector = []
        for idx, val in enumerate(vector):
            new_vector.append(vector[idx] / word_count_found)
        return new_vector


    return None



# define training data
import csv
with open('data/Occupations.csv') as occupationsCsvFile:
    OccupationsList = []
    reader = csv.DictReader(occupationsCsvFile)
    for row in reader:
        occupation_words = splitOccupation(row['Occupation'])
        if len(occupation_words) > 0:
            OccupationsList.append(occupation_words)

occupationsCsvFile.close()

print "Generating word to vec model..."
model = Word2Vec(OccupationsList, min_count=1, size=50)

trainSize = 100000
testSize = 20000

print "Building features and labels..."
trainFeatures = []
trainLabels = []
import csv
with open('data/Occupations.csv') as occupationsCsvFile:
    OccupationsList = []
    reader = csv.DictReader(occupationsCsvFile)
    i = 0
    for row in reader:
        vector = get_sentence_vector(row['Occupation'],model)
        if vector is not None:
            vector.append(getAge(row))
            vector.append(getGender(row))
            trainFeatures.append(vector)
            trainLabels.append(row["Level1Id"])
            i = i + 1
            if i > trainSize + testSize:
                break

occupationsCsvFile.close()

#53.6
# from sklearn.naive_bayes import GaussianNB
# clf = GaussianNB()

#68.6
from sklearn.svm import SVC
clf = SVC(kernel="rbf", C=20, gamma=0.02)

#7500/1000 C=20,gamma - 66.6
# from sklearn.svm import SVC
# clf = SVC(kernel="linear", C=20, gamma=0.1)

# 61% success
# from sklearn.neighbors import KNeighborsClassifier
# clf = KNeighborsClassifier(weights='uniform', n_neighbors=50, algorithm='ball_tree', p=1)

# 63% success
# from sklearn.ensemble import RandomForestClassifier
# clf = RandomForestClassifier(random_state=7)

print "Fitting training set..."
clf.fit(trainFeatures[:trainSize], trainLabels[:trainSize])
print "Score using rf"
print "Scoring training set..."
print clf.score(trainFeatures[:trainSize], trainLabels[:trainSize])
print "Scoring test set..."
print clf.score(trainFeatures[trainSize:trainSize+testSize], trainLabels[trainSize:trainSize+testSize])
print "Done"

# fit a 2d PCA model to the vectors
# X = model[model.wv.vocab]
# pca = PCA(n_components=2)
# result = pca.fit_transform(X)
# # create a scatter plot of the projection
# pyplot.scatter(result[:, 0], result[:, 1])
# words = list(model.wv.vocab)
# for i, word in enumerate(words):
#     pyplot.annotate(word, xy=(result[i, 0], result[i, 1]))
# pyplot.show()

def classify(features_train, labels_train):
    # from sklearn.naive_bayes import GaussianNB
    # clf = GaussianNB()
    from sklearn.svm import SVC
    clf = SVC(kernel="rbf", C=0.01)
    clf.fit(features_train, labels_train)
    return clf


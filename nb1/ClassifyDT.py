def classify(features_train, labels_train):
    # from sklearn.naive_bayes import GaussianNB
    # clf = GaussianNB()
    from sklearn import tree
    clf = tree.DecisionTreeClassifier(min_samples_split=2)
    print "hello"
    clf.fit(features_train, labels_train)
    return clf


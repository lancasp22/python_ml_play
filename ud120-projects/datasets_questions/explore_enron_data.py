#!/usr/bin/python

""" 
    Starter code for exploring the Enron dataset (emails + finances);
    loads up the dataset (pickled dict of dicts).

    The dataset has the form:
    enron_data["LASTNAME FIRSTNAME MIDDLEINITIAL"] = { features_dict }

    {features_dict} is a dictionary of features associated with that person.
    You should explore features_dict as part of the mini-project,
    but here's an example to get you started:

    enron_data["SKILLING JEFFREY K"]["bonus"] = 5600000
    
"""

import pickle

enron_data = pickle.load(open("../final_project/final_project_dataset.pkl", "r"))
print enron_data
print enron_data["PRENTICE JAMES"]["total_stock_value"]
print enron_data["COLWELL WESLEY"]["from_this_person_to_poi"]
print enron_data["SKILLING JEFFREY K"]["exercised_stock_options"]

i = 0
j= 0
k = 0
l = 0
for key in enron_data:
    k = k + 1
    if enron_data[key]['total_payments'] == 'NaN':
        l = l + 1

    if enron_data[key]['poi']:
        print
        j = j + 1
        if enron_data[key]['total_payments'] == 'NaN':
            i = i +1
print k
print l
print i
print j
print float(i) * 100/j
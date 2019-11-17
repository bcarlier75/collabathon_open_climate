import pymongo
import numpy as np
import pandas as pd
from sys import argv

# Set up mongodb database
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["product_Durability_db"]
mycol = mydb[argv[1]]
# myquery = {"address": "Park Lane 38"}
# mydoc = mycol.find(myquery)

# Set up matrix for distance_origin
continents = ["America", "Europe", "Asia", "Africa", "Australia"]
d = {'America': [0, 2, 2, 2, 2], 'Europe': [2, 0, 1, 1, 3], 'Asia': [2, 1, 0, 1, 1],
     'Africa': [2, 1, 1, 0, 2], 'Australia': [2, 3, 1, 2, 0]}
mat_continents = pd.DataFrame(d, columns=continents, index=continents)

# Query input to fill Scale column
name = 'Iphone 6s'
category = 'Telephony'
placeOfPurchase = 'Africa'
madeIn = 'Europe'
reusable = 0            # 0 for reusable, 1 for recyclable, 2 for none
quality = 5             # 0 to 5, higher is better
mean_cat = 30           # in months, to be calculated with all products of same category !!!
max_cat = 120           # in monts, to be calculated with all products of same category !!!
dur_year = 10
dur_month = 0
dur_day = 0
duration = (dur_year * 12 + dur_month + dur_day/365 * 12) / mean_cat
energyEff = 0           # 0 to 5, lower is better
useofConsumables = 0    # 0 to 2, lower is better
# Search for distance_origin in mat_continents
distance_origin = mat_continents.loc[placeOfPurchase, madeIn]

# Create scoring matrix
index = ['Distance origin', 'Reusable/Recyclable/None', 'Quality', 'Product Life Duration',
         'Energy Efficiency', 'Use of consumables']
mat_s = pd.DataFrame(index=index,
                     columns=['Scale', 'Conversion', 'Weight', 'Category', 'Category Weight'])

# Fill scoring matrix
convrate = np.array([5/3, 5/2, 1, 5/(max_cat/mean_cat), 1, 5/2])
mat_s.loc[:, 'Scale'] = np.array([distance_origin, reusable, quality, duration, energyEff, useofConsumables])
mat_s.loc[:, 'Conversion'] = mat_s.loc[:, 'Scale'] * convrate
mat_s.loc[:, 'Weight'] = np.array([1, 0.4, 0.2, 0.4, 0 if reusable == 2 else 1, 0 if reusable != 0 else 1])
mat_s.loc[:, 'Category'] = np.array(['Carbon Footprint', 'Durability', 'Durability',
                                     'Durability', 'Energy efficiency', 'Waste'])
a = 0.1 * mat_s.loc['Energy Efficiency', 'Weight']
b = 0.1 * mat_s.loc['Use of consumables', 'Weight']
mat_s.loc[:, 'Category Weight'] = np.array([0.3 - (a/3) - (b/3), 0.3 - (a/3) - (b/3), 0.3 - (a/3) - (b/3),
                                            0.3 - (a/3) - (b/3), a, b])

# Calculate score
score = mat_s.loc['Distance origin', 'Conversion'] * mat_s.loc['Distance origin', 'Category Weight'] +\
        (mat_s.loc['Reusable/Recyclable/None', 'Conversion'] * mat_s.loc['Reusable/Recyclable/None', 'Weight'] +
         (5 - (mat_s.loc['Quality', 'Conversion'] * mat_s.loc['Quality', 'Weight'])) +
         (5 - mat_s.loc['Product Life Duration', 'Conversion']) * mat_s.loc['Product Life Duration', 'Weight']) *\
        mat_s.loc['Product Life Duration', 'Category Weight'] +\
        mat_s.loc['Energy Efficiency', 'Conversion'] * mat_s.loc['Energy Efficiency', 'Category Weight'] +\
        mat_s.loc['Use of consumables', 'Conversion'] * mat_s.loc['Use of consumables', 'Category Weight']

print(f" PLD {mat_s.loc['Product Life Duration', 'Scale']}")
print(f" Conversion {(5 - mat_s.loc['Quality', 'Conversion']) * mat_s.loc['Quality', 'Weight']}")
print(mat_s)
print(f'Score: {score}')

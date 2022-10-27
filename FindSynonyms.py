#!/usr/bin/env python
# coding: utf-8


# Libraries 
import sys
import os
import pandas as pd
import pubchempy as pcp
import time
import csv

Infile = 'Breast Drug List.xlsx'
df = pd.read_excel(Infile, engine='openpyxl')

lst_drug = df.values.tolist()
lst_unfound = []

dict_synonyms = {}

for drug in lst_drug:
    drug = drug[0]
    try:
        df1 = pcp.get_synonyms(drug, 'name')

        synonyms = df1[0]['Synonym']

        dict_synonyms[drug] = synonyms

        # print(drug + ' is found')

        time.sleep(1)
    except:
        print(drug + " is invalid drug")
        lst_unfound.append(drug)

Outfile = 'synonyms.csv'
with open(Outfile, 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in dict_synonyms.items():
        writer.writerow([key, value])
    writer.writerow(['unfound',lst_unfound])

print('There are ' + str(len(dict_synonyms)) + ' drugs.')


    
    
    


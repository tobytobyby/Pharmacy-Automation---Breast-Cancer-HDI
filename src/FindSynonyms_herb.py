import os
import time
import pandas as pd
import csv
from FindSynonyms_drug import writeFile
import requests
import json

"""
Exact match herb names:
http://dp2.labqr.com/dpool/get/herb/info?name=丹参&exact=1


Partial match herb names:
http://dp2.labqr.com/dpool/get/herb/info?name=丹参&exact=0
"""

def main():
    Infile = os.path.abspath('./Original/breast cancer herb list.xlsx')
    df = pd.read_excel(Infile, engine='openpyxl')

    lst_herb = df.values.tolist()
    lst_unfound_herb = []

    dict_synonyms_herb_exact = {}
    dict_synonyms_herb_similar = {}

    print(lst_herb)
    print()

    for herb in lst_herb:
        herb = herb[0]
        exact = True
        
        try:
            print("Herb: " + herb)

            api_for_exact = 'http://dp2.labqr.com/dpool/get/herb/info?name='+herb+'&exact=1'
            synonym_exact_json = requests.get(api_for_exact).json()
            synonym_exact_string = synonym_exact_json['content'][0]['synonyms'].replace("。", "").replace("\n", "").split("、")
            print("Synonym for exact drug :")
            print(synonym_exact_string)
            dict_synonyms_herb_exact[herb] = synonym_exact_string

            # time.sleep(1)
        except:
            exact = False
        
        try:
            api_for_similar = 'http://dp2.labqr.com/dpool/get/herb/info?name='+herb+'&exact=0'
            synonym_similar_json = requests.get(api_for_similar).json()
            synonym_similar_strings = synonym_similar_json['content']
            print("Synonym for similar drug :")
            for item in synonym_similar_strings:
                name = item['name']
                synonym_similar_string = item['synonyms'].replace("。", "").replace("\n", "").split("、")
                print(name, synonym_similar_string)
                dict_synonyms_herb_similar[name] = synonym_similar_string      
            
            if (exact == False):
                print(herb + ' is invalid, ' + name + " is found.")
            print()
            print()
        except:
            print(herb + " is invalid herb")
            lst_unfound_herb.append(herb)

    writeFile(os.path.abspath('./Synonyms/synonyms_herb_exact.csv'), dict_synonyms_herb_exact, lst_unfound_herb)
    writeFile(os.path.abspath('./Synonyms/synonyms_herb_similar.csv'), dict_synonyms_herb_similar, lst_unfound_herb)

    print('There are ' + str(len(dict_synonyms_herb_exact)) + ' drugs.')

if (__name__ == "__main__"):
    main()
    
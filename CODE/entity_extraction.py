__author__ = 'pegah'

from pycorenlp import StanfordCoreNLP
import os
import json
from sutime import SUTime

"""Function for extracting Name, organization name and date from a given snippet"""
def extract_entitites(snippet):
    """
    this function gets
    :param snippet: a snippet in English
    :return: and returns back the extracted person name, organization name, location and year in a dictionary namely output
    """

    nlp = StanfordCoreNLP('http://localhost:9000')
    res = nlp.annotate(snippet,
                   properties={
                       'annotators': 'ner', #'sutime'
                       'outputFormat': 'json',
                       #'timeout': 1000,
                   })

    output = {'RN':[], 'U':[], 'Y':[]}

    """ for extracting the university and persons names"""
    for sent in range(len(res['sentences'])):
        for element in res['sentences'][sent]['tokens']:
            if element['ner'] == 'PERSON':
                output['RN'].append(element['word'])
            if element['ner'] == 'LOCATION' or element['ner'] == 'ORGANIZATION':
                output['U'].append(element['word'])


    """ for extracting the years"""
    jar_files = os.path.join(os.path.dirname(__file__), 'jars')
    sutime = SUTime(jars=jar_files, mark_time_ranges=True)
    res = json.dumps(sutime.parse(snippet), sort_keys=True, indent=4)


    for i in range(len(res)):
        if res[i:i+5] == 'value':
            j = i+9
            while res[j] != '"':
                j = j+1
            output['Y'].append(''.join(res[i+9:j]))

    return output

print(extract_entitites('Pegah Alizadeh was born september 21 1983 in Ahvaz, Iran. she finished her PHD at '
                        'University of PARIS13 2016.'))
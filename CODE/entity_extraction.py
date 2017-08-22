__author__ = 'pegah'

from pycorenlp import StanfordCoreNLP
import os
import json
from sutime import SUTime
import textrazor

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
            if element['ner'] == 'ORGANIZATION': #or element['ner'] == 'LOCATION' :
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

#print(extract_entitites('Pegah Alizadeh was born september 21 1983 in Ahvaz, Iran. she finished her PHD at "
#                          "university of PARIS13 2016.'))

#print({'RN': ['Pegah', 'Alizadeh'], 'U': ['University', 'of', 'PARIS13'], 'Y': ['1983-09-21', '2016']})

"""another approach for extracting the entities with their confidence score"""

def extract_entities_textrazor(snippet):
    """
    this function extract two entities (university name, researcher name and numebers)
    and confidence scores using the textrazor package
    :param snippet:
    :return:
    """

    textrazor.api_key = "7b4d6194cabab0a5c05bd34ad0ba423520a4a3d33a0304b9783971c9"

    client = textrazor.TextRazor(extractors=["entities", "topics"])
    response1 = client.analyze(snippet) #"Pegah Alizadeh was born september 21 1983 in Ahvaz, Iran. she finished her PHD at "
                               #"university of PARIS13 2016.")

    output = {'RN':{'entity':[], 'confidenceScore':[]}, 'U':{'entity':[], 'confidenceScore':[]},
          'Y':{'entity':[], 'confidenceScore':[]} }

    for entity in response1.entities():
        #print(entity.json)
        """if list is not empty"""
        if len(entity.freebase_types) > 0:
            if entity.freebase_types[0]  == ['/people/person']: #.__contains__('person'):
                output['RN']['entity'].append( (entity.json['entityId']).split(' ') )
                output['RN']['confidenceScore'].append( entity.confidence_score )
            elif entity.freebase_types[0].__contains__('organization'): #== ['/organization/organization']:
                output['U']['entity'].append( (entity.json['entityId']).split(' ') )
                output['U']['confidenceScore'].append(entity.confidence_score)

        else:
            if 'type' in entity.json:
                if entity.json['type'] == ['Number']:
                    output['Y']['entity'].append((entity.json['entityId']).split(' '))
                    output['Y']['confidenceScore'].append(entity.confidence_score)

    return output

""" for extracting the years"""
def extract_years(snippet, output):
    """
    function extracts the dates and fill them with the computed confidence score of
    function extract_entities_textrazor
    :param snippet:
    :param output:
    :return:
    """
    jar_files = os.path.join(os.path.dirname(__file__), 'jars')
    sutime = SUTime(jars=jar_files, mark_time_ranges=True)
    res = json.dumps(sutime.parse(snippet), sort_keys=True, indent=4)

    dates_list = []
    for i in range(len(res)):
        if res[i:i+5] == 'value':
            j = i+9
            while res[j] != '"':
                j = j+1
            dates_list.append(''.join(res[i+9:j]))


    dic_year = output['Y']
    dates_list_new = {'entity':[], 'confidenceScore': [] }

    for i in range(len(dic_year['entity'])):
        for ele in dates_list:
            if ele.__contains__(dic_year['entity'][i][0]):
                if ele not in dates_list_new['entity']:
                    dates_list_new['entity'].append(ele)
                    dates_list_new['confidenceScore'].append(dic_year['confidenceScore'][i])

    output['Y'] = dates_list_new
    return output

#TODO this funcion needs more work to etract the entities and confidence scores more precosely and better!
def extract_entities_confidence_score(snippet):
    """
    the main function to extract the entities and therir confident score
    :param snippet:
    :return: it returns a dictionary as
    """
    output = extract_entities_textrazor(snippet)
    final_output = extract_years(snippet, output)
    return final_output

#"""Execution test"""
#print(extract_entities_confidence_score("Pegah Alizadeh was born september 21 1983 in Ahvaz, Iran. she finished her PHD at "
#                           "university of PARIS13 2016."))

#extract_entities_textrazor("mfrm")



import json
import re
import os
import yaml

def getMITRETechique(title,tags):
    techniques = []
    hit = ''
    for tag in tags:
        hitRegex = re.search("^[Tt][0-9]+", tag)
        if (hitRegex):
            techniques.append(tag.upper())
    if len(techniques)!=0 :   
        # print (title,techniques)     
        for technique in techniques:
            hit = hit  + ',' + technique
        hit = hit[1:]
        print (title + ';' + hit)

def getSigmaTechniques(title,tags):
    techniques = []
    hit = ''
    for tag in tags:
        hitRegex = re.search("^attack.[t]", tag)
        if (hitRegex):
            techniques.append(tag[7:].upper())
    if len(techniques)!=0 :   
        # print (title,techniques)     
        for technique in techniques:
            hit = hit  + ',' + technique
        hit = hit[1:]
        print (title + ';' + hit)

def countMITRETechniquesTags():
    entries = os.listdir(os.getcwd() + '/CB_feeds')
    for entry in entries:
        with open(os.getcwd() + '/CB_feeds/' + entry) as json_file:
            reports = json.load(json_file)
            for report in reports:
                try:
                    getMITRETechique(report['title'], report['tags'])
                except :
                    pass

def countSigmaTechniqueTags():
    entries = os.listdir('')
    for entry in entries:
        with open(os.getcwd() + '/CB_feeds/' + entry) as json_file:
            reports = json.load(json_file)
            for report in reports:
                try:
                    getMITRETechique(report['title'], report['tags'])
                except :
                    pass
    with open('test.yml') as yaml_file:
        rules = yaml.full_load(yaml_file)
        print(rules['tags'])
        getSigmaTechniques(rules['title'], rules['tags'])


if __name__ == "__main__":
    # countMITRETechniquesTags()
    countSigmaTechniqueTags()
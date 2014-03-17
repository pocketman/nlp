import api
import json
'''
This module deals with i/o of our input
'''

#returns a tuple of our questions (dict with key being qns_id)
def readQuestions(q_loc):
    labels = []
    qs = {}
    with open(q_loc) as file:
        labels = map(lambda x: x.strip(),file.readline().split("\t"))
        for line in file:
            question = {}
            tokens = map(lambda x: x.strip(), line.split("\t"))
            id = 0
            for i in xrange(len(tokens)):
                if labels[i]=='qns_id':
                    id = int(tokens[i])
                    continue
                question[labels[i]]=tokens[i]
            qs[id]=question
    return qs

#tokenize sentences
def tokenize(input_sentence):
    return 



#return the POS of each word
def getPOS(input_sentence):
    if api.corenlp is None:
        raise Exception("CoreNLP is not loaded yet!")
    parse_result = api.corenlp.raw_parse(input_sentence)
    parse_result = parse_result["sentences"][0]
    #parse_result = json.loads(parse_result)
    posInfo = parse_result['words']#3 is the index of pos information
    posMap = {}
    #convert tuple to dictionary
    for info in posInfo:
        posMap[info[0]] = info[1]['PartOfSpeech']
    return posMap

'''
def test():
    result = getPOS("What is your name?")
    for key in result:
        print key + " " + result[key]
'''

    

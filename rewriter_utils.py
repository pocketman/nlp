import api
import json
'''
This module deals with i/o of our input
'''

class RewriterUtils:

    def __init__(self):
        self.parseResult = None

    def parse(self, input_sentence):
        self.parse_result = api.corenlp.raw_parse(input_sentence)
        self.parse_result = self.parse_result["sentences"][0]

        #store infomation
        self.wordList = self.tokenize(input_sentence)
        self.posMap = self.getPOS(input_sentence)

    def tokenize(self, input_sentence):
        words = self.parse_result['words']
        wordList = []
        for info in words:
            wordList.append(info[0])
        return wordList



    #return the POS of each word
    def getPOS(self, input_sentence):
        if api.corenlp is None:
            raise Exception("CoreNLP is not loaded yet!")
        #parse_result = json.loads(parse_result)
        posInfo = self.parse_result['words']#3 is the index of pos information
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

    

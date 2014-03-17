import sys
sys.path.add("../../../")
import api
'''
    This module deals with i/o of our input
    '''

class Parser:
    dependenceRuleMapFile = "rules/dep_rule/dep_rule.txt"
    dependenceRuleMap = None
    def __init__(self):
        self.parseResult = None
        #read the dependence rules from file
        if dependenceRuleMap == None:
            dependenceRuleMap = {}
            file = open(dependenceRuleMapFile)
            for line in file:
                tempList = line.split()
                dependenceRuleMap[tempList[0].strip()] = tempList[1].strip()
        self.depMap = None
    
    
    
    
    def parse(self, input_sentence):
        self.parse_result = api.corenlp.raw_parse(input_sentence)
        self.parse_result = self.parse_result["sentences"][0]
        
        #store infomation
        self.wordList = self.tokenize(input_sentence)
        self.posMap = self.getPOS(input_sentence)
        
        #store dependence rule
        self.depMap = getDependence(input_sentence)
    
    
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
    
    #return the dependence of each word
    def getDependence(self, input_sentence):
        if api.corenlp is None:
            raise Exception("CoreNLP is not loaded yet!")
                #parse_result = json.loads(parse_result)
                depInfoList = self.parse_result['dependencies']#3 is the index of pos information
                return processDependence(depInfoList)
            
            #adjust the order of dependence according to rules
            def processDependence(self, depInfoList):
                depMap = {}
                for depInfo in depInfoList:
                    if dependenceRuleMap.has_key(depInfo[0]) and dependenceRuleMap[depInfo[0]]:
                        depMap[depInfo[2]] = depInfo[1]
                    else:
                        depMap[depInfo[1]] = depInfo[2]
                return depMap
            
            
            
            '''
                def test():
                result = getPOS("What is your name?")
                for key in result:
                print key + " " + result[key]
                '''



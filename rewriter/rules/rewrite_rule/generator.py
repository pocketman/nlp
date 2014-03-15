import nltk
import json
import sys
sys.path.append("../../")
import parser
from entity import Word
class ModelRewriter:
    rewriteRules = None
    rewriteRuleFileName = "model.txt"




    @staticmethod
    def loadModel():
        inputFile = open("model.txt")
        modelJsonString = inputFile.read()
        inputFile.close()
        print modelJsonString
        modelMap = json.loads(modelJsonString)
        ModelRewriter.rewriteRules = modelMap
        return modelMap

    def __init__(self):
        if ModelRewriter.rewriteRules is None:
            ModelRewriter.rewriteRules = ModelRewriter.loadModel()


    #this is the only method the user need to invoke
    @staticmethod
    def generateQuestions(inputSentence):
        sentencePOS = ModelRewriter.parseSentence(inputSentence)
        nearestModels = ModelRewriter.getNearestModel(sentencePOS)
        questions = []
        for model in nearestModels:
            tempQuestionList = ModelRewriter.generateQuestionFromModel(model, inputSentence)
            questions += tempQuestionList
        return questions


    @staticmethod
    def parseSentence(sentence):
        questionWordMap = {}
        text = nltk.word_tokenize(sentence)
        posTag = nltk.pos_tag(text)
        for i in xrange(len(text)):
            word = Word()
            word.index = i
            word.pos = posTag[i][1]
            questionWordMap[text[i]] = word

        questionWordMap["WHOLE-SENTENCE-LIST"] = text
        return questionWordMap

    @staticmethod
    def getNearestModel(sentencePOSList):
        '''
        return the nearest model
        '''
        nearestModelList = []
        modelList = ModelRewriter.rewriteRules["template"]
        for model in modelList:
            posList = model["pos"]
            if ModelRewriter.comparePOSList(sentencePOSList, posList):
                nearestModelList.append(model)
        return nearestModelList

    @staticmethod
    def comparePOSList(templateModelPOSList, newModelPOSList):
        if len(templateModelPOSList) == len(newModelPOSList):
            return False
        else:
            for i in xrange(len(templateModelPOSList)):
                try:
                    if templateModelPOSList[i] != newModelPOSList[i]:
                        return False
                except:
                    print i

            return True


    @staticmethod
    def generateQuestionFromModel(model, inputSentence):
        sentenceToken = nltk.word_tokenize(inputSentence)
        questions = []
        if model.has_key("Easy"):
            questionList = model["Easy"]
            for questionMap in questionList:
                question = ModelRewriter.generateSingleQuestion(questionMap, sentenceToken)
                if question is not None:
                    questions += question   #merge two lists



        elif model.has_key["Medium"]:
            pass
        elif model.has_key["Hard"]:
            pass
        elif model.has_key["Ghost"]:
            pass

        return questions



    @staticmethod
    def generateSingleQuestion(modelMap, sentenceToken):

        question = modelMap["question"]
        indexList = modelMap["index"]

        questionToken = nltk.word_tokenize(question)

        questionString = ""
        indexList = indexList.strip().split()
        for i in xrange(len(indexList)):
            if indexList[i] == "-":
                try:
                    questionString += questionToken[i]
                except:
                    print "error------"
                    print questionToken[i]

            else:
                try:
                    questionString += sentenceToken[int(indexList[i].strip())]
                except:
                    print sentenceToken
                    print indexList
                    print indexList[i]

































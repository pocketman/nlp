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
        modelMap = json.loads(modelJsonString)
        ModelRewriter.rewriteRules = modelMap
        return modelMap

    def __init__(self):
        if ModelRewriter.rewriteRules is None:
            ModelRewriter.rewriteRules = ModelRewriter.loadModel()


    #this is the only method the user need to invoke
    @staticmethod
    def generateQuestions(inputSentence):
        print inputSentence
        sentencePOS = ModelRewriter.getPOSList(inputSentence)
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
        if len(templateModelPOSList) != len(newModelPOSList):
            return False
        else:
            print templateModelPOSList
            print newModelPOSList
            for i in xrange(len(templateModelPOSList)):
                tempTemplate = unicode(templateModelPOSList[i])
                tempNew = unicode(newModelPOSList[i])
                if tempTemplate != tempNew:
                    return False
            return True

    @staticmethod
    def getPOSList(sentence):
        tokenList = nltk.word_tokenize(sentence)
        posList = nltk.pos_tag(tokenList)
        resultList = []
        for temp in posList:
            resultList.append(temp[1])
        return resultList


    @staticmethod
    def generateQuestionFromModel(model, inputSentence):
        sentenceToken = nltk.word_tokenize(inputSentence)
        questions = []
        if model.has_key("Easy"):
            questionList = model["Easy"]
            for questionMap in questionList:
                question = ModelRewriter.generateSingleQuestion(questionMap, sentenceToken)
                if question is not None:
                    questions.append(question)   #merge two lists

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

        questionToken = nltk.word_tokenize(question.strip())

        questionString = ""
        indexList = indexList.strip().split()
        for i in xrange(len(indexList)):
            if indexList[i] == "-":
                questionString += questionToken[i]

            else:
                questionString += sentenceToken[int(indexList[i].strip())]
            questionString += " "
        return questionString.strip()






if __name__ == "__main__":
    print ModelRewriter.getPOSList("He received two yellow cards as Chelsea lost at White Hart Lane for the first time since 1987.")



























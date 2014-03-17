import nltk
import json
import sys
sys.path.append("../../")
import parser
from entity import Word
class TrainQuestionModel:


    @staticmethod
    def getFileContent(inputFile):
        file = open(inputFile)
        textInfo = file.read()
        file.close()
        print textInfo
        textInfo = json.loads(textInfo)
        return textInfo

    @staticmethod
    def train(inputFile, outputFile):
        fileContent = TrainQuestionModel.getFileContent(inputFile)
        models = fileContent["template"]
        outputMap = {}
        outputModelList = []
        for model in models:
            singleModelMap = {}
            #record origin file into the json string
            singleModelMap["origin"] = model["origin"]
            originalSentence = model["origin"]
            originWordMap = TrainQuestionModel.parseSentence(originalSentence)
            #record pos filed into the json string
            singleModelMap["pos"] = TrainQuestionModel.getPOSList(originWordMap)



            #deal with easy cases
            if model.has_key("Easy"):
                easyQuestionList = []
                for sentence in model["Easy"]:
                    questionWordMap = TrainQuestionModel.parseSentence(sentence)
                    resultMap = TrainQuestionModel.convert(originWordMap, questionWordMap, originWordMap["WHOLE-SENTENCE-LIST"], questionWordMap["WHOLE-SENTENCE-LIST"], sentence)
                    easyQuestionList.append(resultMap)
                singleModelMap["Easy"] = easyQuestionList
            outputModelList.append(singleModelMap)





            if model.has_key("Moderate"):
                pass

            if model.has_key("Hard"):
                pass

            if model.has_key("Ghost"):
                pass
        outputMap["template"] = outputModelList
        TrainQuestionModel.saveJsonToFile("model.txt", outputMap)
        return outputMap

    @staticmethod
    def saveJsonToFile(outputFileName, outputMap):
        outputFile = open(outputFileName, "w")
        outputFile.write(json.dumps(outputMap))
        outputFile.close()


    @staticmethod
    def convert(sentenceWordMap, questionWordMap, sentenceTokenList, questionTokenList, question):
        resultMap = {}
        resultMap["question"] = question
        pos = ""
        for token in questionTokenList:
            pos += questionWordMap[token].pos + " "
        pos.strip()
        index = ""
        for token in questionTokenList:
            if sentenceWordMap.has_key(token):
                index += str(sentenceWordMap[token].index) + " "
            else:
                index += "-" + " "
        index.strip()
        resultMap["pos"] = pos
        resultMap["index"] = index
        return resultMap


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
    def getPOSList(wordMap):
        wordList = wordMap["WHOLE-SENTENCE-LIST"]
        resultList = []
        for token in wordList:
            resultList.append(wordMap[token].pos)
        return resultList



if __name__ == "__main__":
    train = TrainQuestionModel()
    train.train("train.txt", "result.txt")


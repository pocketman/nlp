import nltk.data
from generator import ModelRewriter


if __name__ == "__main__":
    inputFile = open("jiaxing.txt")
    inputText = inputFile.read()
    inputFile.close()

    sent_detector = nltk.data.load("tokenizers/punkt/english.pickle")
    sentenceList = sent_detector.tokenize(inputText.strip())
    print 
    questionList = []
    ModelRewriter.loadModel()
    for sentence in sentenceList:
        question = ModelRewriter.generateQuestions(sentence)
        questionList += question

    print "----------"
    print len(questionList)

import keysearch
import extractor
import api

q = None
article = None

#parse a couple sentences
def parse(s):
    sentence = api.parseS(s)
    return sentence

#Set the article to draw information from
def readA(fileloc):
    global article
    article = api.parsefile(fileloc)
    keysearch.trainIR(article)

#Set the question to be asked
def askQ(s):
    global q
    q = keysearch.parseQ(s)

#Fetches the top ranked sentences
def getrank():
    return keysearch.mostRelevant(q,article)

#reload functions
def myreload():
    reload(keysearch)
    reload(extractor)
    keysearch.trainIR(article)

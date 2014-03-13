import keysearch
import api

q = None
article = None

#Set the article to draw information from
def readA(fileloc):
    global article
    article = api.parsefiles(fileloc)
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
    keysearch.trainIR(article)

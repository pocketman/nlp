import keysearch as ks
import extractor as ex
import api
import json

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
    ks.trainIR(article)

#Set the question to be asked
def askQ(s):
    global q
    q = ks.parseQ(s)
    return getrank()
    '''svo = ex.getQ(0,parse(s)[0])
    if not svo:
        return "I don't know"
    for r in ranks:
        result = ex.getYN(svo, parse(r))
        if result==1:
            return "Yes"
        elif result == -1:
            return "No"
    return "I don't know"'''

#Fetches the top ranked sentences
def getrank():
    return ks.mostRelevant(q,article)


#reload functions
def myreload():
    reload(ks)
    reload(ex)
    ks.trainIR(article)

def toJson(s, name):
    f = open(name, 'w')
    f.write(json.dumps(s))
    f.close()
def fromJson(name):
    stuff = []
    f = open(name)
    for l in f:
        stuff.append(json.loads(l))
    f.close()
    return stuff

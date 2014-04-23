import keysearch as ks
import extractor as ex
import api
import json
import collections
import sys

q = None
article = None

STARTREK = 'data/set4/a8.txt'
THEARTIST = 'data/set4/a1.txt'
MESSI = 'data/set1/a7.txt'

#parse a couple sentences
def parse(s):
    sentence = api.parseS(s)
    return sentence

#Set the article to draw information from
def readA(fileloc):
    article = []
    V = collections.Counter()
    N = 0
    article = api.parsefile(fileloc)
    N = ks.trainIR(article, V)
    sents = None
    return [article, V, N, sents]

#Set the question to be asked
def askQ(s, article_obj):
    q = ks.parseQ(s)
    return getrank(q, article_obj)
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
def getrank(q, article_obj):
    article = article_obj[0]
    V = article_obj[1]
    N = article_obj[2]
    sents = article_obj[3]
    return ks.mostRelevant(q,article, V, N, sents)


#reload functions
def myreload():
    reload(ks)
    reload(ex)

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


def getQ(questions):
    f = open(questions)
    firstline = f.readline().strip()
    lbls = {}
    for i,tok in enumerate(firstline.split()):
        lbls[tok] = i
    questions = []
    for line in f:
        toks = line.strip().split('\t')
        q = {}
        if len(toks)<len(lbls):
            print len(toks), len(lbls)
            continue
        q['qns_text'] = toks[lbls['qns_text']]
        q['answer'] = toks[lbls['answer']]
        q['article_title'] = toks[lbls['article_title']]
        q['path'] = 'data/'+toks[lbls['path']]+'.txt'
        q['type'] = toks[lbls['qns_difficulty_by_questioner']]
        if len(questions)==0 or\
           q['qns_text']!=questions[-1]['qns_text']:
            questions.append(q)
    f.close()
    return questions

def evalAlgo():
    q = getQ('questions.txt')
    i = 0
    out = raw_input('File to write: ')
    article_name = q[i]['path']
    types = collections.Counter()
    total = collections.Counter()
    a_obj = readA(article_name)
    while i<len(q):
        output = open(out,'a+')
        if q[i]['path']!=article_name:
            article_name = q[i]['path']
            a_obj = readA(article_name)
        outstr = q[i]['type']+' | '+q[i]['qns_text']+ '\n'+ str(askQ(q[i]['qns_text'], a_obj)[0])+'\n'+q[i]['answer']+'\n'
        output.write(outstr)
        output.close()
        i+=1
        print i



def main():
    if len(sys.argv)<2:
        return
    qloc = sys.argv[2]
    text = sys.argv[1]
    a = readA(text)
    f = open(qloc)
    for line in f:
        print askQ(line,a)[0][0]

if __name__=="__main__":
    main()

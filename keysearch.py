import api
import collections
import math
import simp
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
import subprocess
import os
SEMCOR_IC = wordnet_ic.ic('ic-semcor.dat')

#load corenlp if not loaded
if not (api.corenlp):
    api.getcorenlp()

corenlp = api.corenlp

sim_scores = {}

#ignore these POS
IGNORE = ['DT','.',',','\'']
#weights given to POS
#POS not in this are given default value of 1
POSWGHT = {'RB': 0.7,\
           'RBR':0.7,\
           'RBS':0.7,\
           'JJ': 1.2,\
           'JJR':1.2,\
           'JJS':1.2,\
           'IN': 0.4,\
           'NN': 1.7,\
           'NNS':1.7,\
           'NNP':2.0,\
           'VB': 1.5,\
           'VBD': 1.5,\
           'VBG': 1.5,\
           'VBN': 1.5,\
           'VBP': 1.5,\
           'VBZ': 1.5,\
           'WDT':0.2,\
           'WP':0.2,\
           'POS': 0.01,\
           'DET': 0,\
           'WRB': 0,\
           '.': 0}
DEBUG = False
def pdbg(s, t1 = 1, t2= 0):
    if DEBUG and t1>t2:
        print s
#words that add little to no value
BL = ['ever', 'have', 'how', 'do', 'that', 'be']
DWGHT = 1.0 # default weight
def parseQ(q):
    question = api.parseS(q)
    return question[0]
def askQ(question, document):
    article = parsefile(document)
    q = parseQ(question)

def trainIR(article, V):
    for sentence in article:
        seen = {}
        for w in sentence:
            word = w['lemma']
            if not word in seen:
                seen[word] = True
                V[word]+=1
    return len(article)

def mostRelevant(q, article, V, N, sents):
    dictq = {}
    q = q[1:]
    for tok in q:
        dictq[tok['lemma']] = tok['POS']
    sentencerank = []
    simscores = simScore2([q], article)
    for i in range(len(article)):
        s = article[i]
        (score, matched) = cosDist(dictq, s, V, N)
        #(simscore, matched2) = simScore(api.toString(q), dictq, s, matched = matched)
        simscore = 0
        if len(article)==len(simscores):
            simscore = simscores[i]
        #simscore = 1.0/(1+math.exp(-(simscore-0.5)))
        #pdbg(str(score)+","+str(simscore)+"|"+ api.toString(s),t1=simscore+score, t2=2)
        score = score + 6*simscore
        sentencerank.append((api.toString(article[i]), score, simscore, matched))
    sentencerank = sorted(sentencerank, key = lambda t: t[1], reverse=True)
    return sentencerank

def simScore2(questions, article):
    qs = open('semilar/q','w')
    sents = open('semilar/s', 'w')
    for q in questions:
        qs.write(api.toString(q)+"\n")
    for s in article:
        sents.write(api.toString(s)+"\n")
    qs.close()
    sents.close()
    scores = []
    os.chdir('semilar')
    rc = subprocess.call('run q s > /dev/null 2>/dev/null', shell=True)
    os.chdir('..')
    results = open('semilar/out')
    for l in results:
        toks = l.split('\t')
        qindex = int(toks[0])
        sindex = int(toks[1])
        val = float(toks[2])
        scores.append(val)
    results.close()
    return scores
def simScore(question, qtoks, stoks, matched = None):
    total = 0
    dbg = []
    for qw in qtoks:
        if qw in BL:
            continue
        qpos = qtoks[qw] #not used in current wsd algo
        wsdq = getSynset(question, qw)
        if not wsdq or qw in matched:
            continue
        maxsofar = 0
        qname = qw
        wname = ""
        for i in range(len(stoks)):
            tok = stoks[i]
            word = tok['lemma']
            wsdw = tok['WS']
            score = 0
            if word in matched or word in BL:
                continue
            if wsdw:
                name = wsdq.name+","+wsdw.name
                if name in sim_scores:
                    score = sim_scores[name]
                else:
                    lchsim = 0
                    linsim = 0
                    if wsdw.pos == wsdq.pos:
                        lchsim = wsdw.lch_similarity(wsdq)
                        if not lchsim:
                            lchsim = 0
                        lchsim/=2
                        linsim = wsdw.lin_similarity(wsdq, SEMCOR_IC)
                    wupsim = wsdw.wup_similarity(wsdq)
                    if not wupsim:
                        wupsim = 0
                    if not linsim:
                        linsim = 0
                    score = linsim
                    sim_scores[name] = score
                    sim_scores[wsdw.name+","+wsdq.name]=score
                if score>maxsofar:
                    wname = word
                    maxsofar = score
        total += maxsofar
        dbg.append((qname,wname, maxsofar))
    return (total, dbg)
def cosDist(q, s, V, N):
    score = 0
    start = len(s)
    end = 0
    numcorrect = 0
    debug = ""
    matched=[]
    for qw in q:
        if qw in BL or (q[qw] in POSWGHT and POSWGHT[q[qw]]==0):
            continue
        qpos = q[qw]
        v = 0
        matchedword = ""
        for i in range(len(s)):
            tok = s[i]
            word = tok['lemma']
            pos = tok['POS']
            weight = DWGHT
            multiplier = 1
            if pos in POSWGHT and POSWGHT[pos]==0:
                continue
            if word==qw:
                if pos in POSWGHT:
                    weight = POSWGHT[pos]
                if pos==qpos:
                    multiplier*=1.5
                newv = multiplier*weight*math.log(float(N)/V[word])
                if newv>v:
                    if i<=start:
                        start=i
                    if i>=end:
                        end = i+1
                    numcorrect+=1
                    debug+=" "+word+" "
                    v = newv
        if v>0:
            matched.append(qw)
        score+=v
    avgdist = 0
    if end-start>0:
        avgdist = (end-start)/float(numcorrect)
        score = score-0.01*avgdist
    pdbg(debug+","+str(-avgdist), t1=score, t2=10)
    return (score,matched)

def getSynset(s,w):
    return simp.getSynset(s,w)

    '''wpos = ""
    if 'JJ' in pos:
        wpos = "s"
    elif 'RB' in pos:
        wpos = "r"
    elif 'NN' in pos:
        wpos = "n"
    elif 'VB' in pos:
        wpos = 'v'
        '''




#question classifier
#Noun Phrase Key Words
#1 - object
#2 - time
#3 - place
#4 - person
CATS = ['Y/N', 'object', 'time', 'place', 'person']
NPKW = {'what':1,\
        'when':2,\
        'where':3,\
        'which':1,\
        'who': 4,\
        'whose': 4,\
        'whom': 4,\
        'why': 1,\
        'how': 1}

YN = {'is': 0,\
      'can': 0,\
      'have': 0,\
      'do': 0,\
      'would': 0}
def classifyQ(q):
    for tok in q:
        word = tok['word'].lower()
        if word in NPKW:
            print CATS[NPKW[word]]
            return NPKW[word]
        elif word in YN:
            print CATS[YN[word]]
            return YN[word]
    print 'Not a question.'
    return -1


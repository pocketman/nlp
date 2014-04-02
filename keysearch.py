import api
import collections
import math

#load corenlp if not loaded
if not (api.corenlp):
    api.getcorenlp()

corenlp = api.corenlp

#ignore these POS
IGNORE = {'DT','.',',','\''}
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
           'VB': 1.3,\
           'VBD': 1.3,\
           'VBG': 1.3,\
           'VBN': 1.3,\
           'VBP': 1.3,\
           'VBZ': 1.3,\
           'WDT':0.2,\
           'WP':0.2,\
           'DET': 0,\
           'WRB': 0,\
           '.': 0}
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

def mostRelevant(q, article, V, N):
    dictq = {}
    for tok in q:
        dictq[tok['lemma']] = tok['POS']
    sentencerank = []
    for i in range(len(article)):
        s = article[i]
        sentencerank.append((api.toString(article[i]), cosDist(dictq, s, V, N)))
    sentencerank = sorted(sentencerank, key = lambda t: t[1], reverse=True)
    return sentencerank

def cosDist(q, s, V, N):
    alreadyseen = {}
    score = 0
    start = len(s)
    end = 0
    numcorrect = 0
    for i in range(len(s)):
        tok = s[i]
        word = tok['lemma']
        pos = tok['POS']
        weight = DWGHT
        if word in q:
            numcorrect+=1
            if i<=start:
                start = i
            if i>=end:
                end = i+1
            if pos in POSWGHT:
                weight = POSWGHT[pos]
            if not word in alreadyseen:
                score+=weight*math.log(N/V[word])
                alreadyseen[word] = {}
            if not pos in alreadyseen[word]:
                if pos == q[word]:
                    score+=2*weight*math.log(N/V[word])
                else:
                    score+=weight*math.log(N/V[word])
                alreadyseen[word][pos] = True
    if end-start>0:
        avgdist = (end-start)/numcorrect
        score = score-avgdist/(len(q)+len(s))
    return score



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


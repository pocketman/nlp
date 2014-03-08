import api
import collections
import math

#load corenlp if not loaded
if not (api.corenlp):
    api.getcorenlp()

corenlp = api.corenlp

#ignore these POS
IGNORE = {'DT','.',',','\''}
#parameters for IR
V = collections.Counter()
N = 0
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
           'VB': 1.7,\
           'VBD': 1.7,\
           'VBG': 1.7,\
           'VBN': 1.7,\
           'VBP': 1.7,\
           'VBZ': 1.7,\
           'WDT':0.2,\
           'WP':0.2} 
DWGHT = 1.0 # default weight
def parseQ(q):
    question = []
    parse = corenlp.raw_parse(q)
    for w in parse['sentences'][0]['words']:
        tok={}
        tok['word'] = w[0]
        tok['NER'] = w[1]['NamedEntityTag']
        tok['POS'] = w[1]['PartOfSpeech']
        if not (tok['POS'] in IGNORE):
            question.append(tok)
    return question
def askQ(question, document):
    article = parsefile(document)
    q = parseQ(question)
    
def trainIR(article):
    global V
    global N
    N = len(article)
    for sentence in article:
        seen = {}
        for w in sentence:
            word = w['word']
            if not word in seen:
                seen[word] = True
                V[word]+=1

def mostRelevant(q, article):
    dictq = {}
    for tok in q:
        dictq[tok['word']] = tok['POS']
    sentencerank = []
    for s in article:
        sentencerank.append((api.toString(s), cosDist(dictq, s)))
    sentencerank = sorted(sentencerank, key = lambda t: t[1], reverse=True)
    return sentencerank

def cosDist(q, s):
    alreadyseen = {}
    score = 0
    for tok in s:
        word = tok['word']
        pos = tok['POS']
        weight = DWGHT
        if word in q:
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
    return score

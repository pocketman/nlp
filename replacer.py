import subprocess
import sys
import api
import collections
from nltk.corpus import wordnet as wn
from random import randint

if not api.corenlp:
    api.getcorenlp()

#words with these POS are to be replaced with
#synonyms/antonyms/hypernyms/hyponyms
REP = ['NN', 'NNP', 'NNPS', 'JJ']


def getQuestions(filename, num):
    output = subprocess.check_output('askaux '+filename+' '+num, shell=True)
    output = output.split("\n")
    questions = []
    for q in output:
        if len(q)>0:
            questions.append(q.split("\t")[0])
    return questions

def replaceQ(q, w1, w2, i):
    return q.replace(w1,w2.replace('_', ' '), i)
def processQ(q):
    parsed = api.parseS(q)[0]
    wc = collections.Counter()
    for tok in parsed:
        wc[tok['word']]+=1
        if tok['POS'] in REP and tok['WS'] and tok['NER']=='O':
            ss = tok['WS']
            newword = tok['word']
            if randint(0,1) and ss.hypernyms():
                #use hypernym
                newword = ss.hypernyms()[randint(0,len(ss.hypernyms())-1)].lemmas[0].name
            elif ss.lemmas:
                #use lemmas
                newword = ss.lemmas[randint(0,len(ss.lemmas)-1)].name
            q = replaceQ(q,tok['word'],newword,wc[tok['word']])
    return q

def main(filename, num):
    questions = getQuestions(filename, num)
    numreplaced = 0
    num = len(questions)*0.3
    for i in range(len(questions)):
        if numreplaced < num:
            print processQ(questions[i])
            numreplaced+=1
        else:
            print questions[i]

if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])

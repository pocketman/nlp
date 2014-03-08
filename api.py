from corenlp import StanfordCoreNLP

CORENLPDIR = 'stanford-corenlp-full-2013-11-12'

corenlp = None

def showtags(sentences):
    for s in sentences:
        string = ""
        for tok in s:
            string += "("+tok['word']+","+tok['POS']+","+tok['NER']+")"
        print string

def getcorenlp():
    global corenlp
    corenlp = StanfordCoreNLP(CORENLPDIR)
    return corenlp
    
def parsefiles(fileloc):
    sentences=[]
    if corenlp==None:
        print "CoreNLP Not loaded"
        return None
    with open(fileloc) as file:
        for line in file:
            parse = corenlp.raw_parse(line)
            for l in parse['sentences']:
                sentence = []
                for w in l['words']:
                    token = {}
                    token['word'] = w[0]
                    token['NER'] = w[1]['NamedEntityTag']
                    token['POS'] = w[1]['PartOfSpeech']
                    sentence.append(token)
                sentences.append(sentence)
    return sentences

def toString(sentence):
    s = ""
    for t in sentence:
        s+=t['word']+" "
    return s[:-1]

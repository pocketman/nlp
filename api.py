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

def parseS(s):
    parse = corenlp.raw_parse(s)
    sentences = []
    for l in parse['sentences']:
        sentence = []
        for w in l['words']:
            token = {}
            token['word'] = w[0]
            token['NER'] = w[1]['NamedEntityTag']
            token['POS'] = w[1]['PartOfSpeech']
            token['lemma'] = w[1]['Lemma']
            sentence.append(token)
        sentences.append(sentence)
    if 'coref' in parse:
        coref(parse['coref'],sentences)
    return sentences

header_len = 30
def parsefile(fileloc):
    sentences=[]
    if corenlp==None:
        print "CoreNLP Not loaded"
        return None
    info=""
    result = []
    with open(fileloc) as file:
        for line in file:
            if len(line)>header_len:
                sentences = parseS(line)
                result.extend(sentences)
    return result

#define a max reference length
#if the reference pointed to exceeds this number of tokens then we can assume coref failed
MAX = 4
def coref(cf, s):
    for group in cf:
        for entities in group:
            a = entities[0]
            b = entities[1]
            sena = a[1]
            senb = b[1]
            heada = a[2]
            headb = b[2]
            if 'PRP' in s[sena][heada]['POS']:
            #replace a
                sub = s[senb][b[3]:b[4]]
                if len(sub)>MAX:
                    continue
                p1 = s[sena][:a[3]]
                p2 = s[sena][a[4]:]
                s[sena] = p1+sub+p2
            elif 'PRP' in s[senb][headb]['POS']:
            #replace b
                sub = s[sena][a[3]:a[4]]
                if len(sub)>MAX:
                    continue
                p1 = s[senb][:b[3]]
                p2 = s[senb][b[4]:]
                s[senb] = p1+sub+p2


def toString(sentence):
    s = ""
    for t in sentence:
        s+=t['word']+" "
    return s[:-1]

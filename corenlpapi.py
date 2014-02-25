import pexpect
import sys
import xml.etree.ElementTree as ET
import time

CWD = 'stanford-corenlp-full-2014-01-04/'

listcommand = 'java -cp stanford-corenlp-3.3.1.jar:stanford-corenlp-3.3.1-models.jar:xom.jar:joda-time.jar:jollyday.jar:ejml-0.23.jar -Xmx1g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,ner,parse -listfile '
command = 'java -cp stanford-corenlp-3.3.1.jar:stanford-corenlp-3.3.1-models.jar:xom.jar:joda-time.jar:jollyday.jar:ejml-0.23.jar -Xmx1g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,ner,parse -file ../'

def gettags(xmlloc):
    tree = ET.parse(xmlloc)
    root = tree.getroot()[0][0]
    sentences = []
    for sentence in root.findall('sentence'):
        mysent = []
        for token in sentence.find('tokens').findall('token'):
            mysent.append({'word':token.find('word').text,'POS':token.find('POS').text, 'NER':token.find('NER').text})
        sentences.append(mysent)
    return sentences

def showtags(sentences):
    for s in sentences:
        string = ""
        for tok in s:
            string += "("+tok['word']+","+tok['POS']+","+tok['NER']+")"
        print string
            
def process(file):
    child = pexpect.spawn(command+file, cwd=CWD)
    child.logfile = sys.stdout
    child.expect(pexpect.EOF, timeout=sys.maxint)

def annotate(file):
    process(file)
    return gettags(CWD+file+".xml")

def demo(file):
    showtags(annotate(file))


if __name__ == "__main__":
    filelist = sys.argv[1] #file containing the names of all files to be processed
    demo(filelist)

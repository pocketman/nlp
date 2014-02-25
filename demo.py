import pexpect
import sys
import xml.etree.ElementTree as ET
import time

listcommand = 'java -cp stanford-corenlp-3.3.1.jar:stanford-corenlp-3.3.1-models.jar:xom.jar:joda-time.jar:jollyday.jar:ejml-0.23.jar -Xmx1g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,ner,parse -listfile '
command = 'java -cp stanford-corenlp-full-2014-01-04 stanford-corenlp-3.3.1.jar:stanford-corenlp-3.3.1-models.jar:xom.jar:joda-time.jar:jollyday.jar:ejml-0.23.jar -Xmx1g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,ner,parse -file '

def read(xmlloc):
    tree = ET.parse(xmlloc)
    root = tree.getroot()[0][0]
    sentences = []
    for sentence in root.findall('sentence'):
        mysent = []
        for token in sentence.find('tokens').findall('token'):
            mysent.append({'word':token.find('word').text,'POS':token.find('POS').text})
        sentences.append(mysent)
    return sentences

def showsen(sentences):
    for s in sentences:
        string = ""
        for tok in s:
            string += "("+tok['word']+","+tok['POS']+")"
        print string
            
def run(file):
    child = pexpect.spawn(command+file)
    child.logfile_read = sys.stdout
    while(child.isalive()):
        time.sleep(500)
    sentences = read(file+".xml")
    showsen(sentences)
    

if __name__ == "__main__":
    filelist = sys.argv[1] #file containing the names of all files to be processed
    run(filelist)

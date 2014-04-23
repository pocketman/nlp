import api
import sys
import splitter

if not api.corenlp:
    api.getcorenlp()

def containsPronoun(s):
    for tok in s:
        if 'PRP' in  tok['POS']:
            return True
    return False
def main(fileloc, out):
    article = api.parsefile(fileloc)
    fout = open(out, 'w')
    for s in article:
        if not containsPronoun(s):
            fout.write(api.toString(s)+"\n")
    fout.close()
    return

if __name__=="__main__":
    main(sys.argv[1], sys.argv[2])

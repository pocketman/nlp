
import sys,copy
from nltk.corpus import wordnet as wn

def convert(sentence):
    out = []
    for wd in sentence:
        s = wn.synsets(wd['word'])
        if len(s)>0:
            wd['word'] = s[0].lemmas[0].name
        out.append(wd)
    return out

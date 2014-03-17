
import sys,copy
from nltk.corpus import wordnet as wn

def convert(sentence):
    out = []
    for wd in sentence:
        l = wn.lemmas(wd['word'])[0]
        wd['word'] = l.name
        out.append(wd)
    return out

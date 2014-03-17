
import sys,copy
from nltk.corpus import wordnet as wn

def convert(sentence):
    out = []
    for wd in sentence:
        ll = wn.lemmas(wd['word'])
        if len(ll)>0:
            wd['word'] = ll[0].name
        out.append(wd)
    return out

import sys
sys.path.append('pywsd')
from lesk import simple_lesk


def getSynset(s, word):
    return simple_lesk(s, word)


import api, extractor
import StringIO
from collections import defaultdict

stuff = ['appos', 'csubj', 'rcmod', 'advcl']
subjects = ['subj', 'nsubj', 'csubjpass', 'nsubjpass']
if api.corenlp is None:
    api.getcorenlp()

class pTree:

    def __init__(self,w,c):
        self.parent = None
        self.word = w
        self.children = c

    def addChild(self,n,rel):
        self.children.append((n,rel))

def order(s):
    return int(s[(s.rfind('-')+1):])


def ioTraverse(t,stream):
    o = order(t.word)
    for (x,y) in t.children:
        if order(x.word) < o:
            if y not in stuff:
                if y[:4] == 'prep':
                    stream.write(y[5:]+' ')
                ioTraverse(x,stream)
    stream.write(t.word[:t.word.rfind('-')])
    stream.write(' ')
    for (x,y) in t.children:
        if y not in stuff and order(x.word) > o:
            if y[:4] == 'prep':
                stream.write(y[5:]+' ')
            ioTraverse(x,stream)


def split(s):
    dep = api.corenlp.raw_parse(s)['sentences'][0]['indexeddependencies']

    treenodes = {}
    treenodesmod = {}
    for w in dep:
        node = pTree(w[2], [])
        treenodes[w[2]] = node

    for w in dep[1:]:
        treenodes[w[1]].addChild(treenodes[w[2]], w[0])

    s = StringIO.StringIO()

    ioTraverse(treenodes[dep[0][2]], s)

    s.write('.')

    return s.getvalue()


#    words = [x[2] for x in dep]
#    par = range(len(dep))
#    wtoi = dict(zip(words, par))
#    top = [dep[0]]
#    for i in xrange(1,len(dep)):
#        if dep[i][0] in stuff:
#            top.append(dep[i])
#        else:
#            par[i] = wtoi[dep[i][1]]
#        for j in xrange(len(par)):
#            if par[j] == i:
#                par[j] = par[i]

   # consolid = defaultdict(list)
   # for i in xrange(len(dep)):
   #     consolid[par[i]].append(dep[i])

#    mainsubj = cosolid[0][2]

#    for i in consolid[0]:
 #       if i[0] in subjects:
  #          mainsubj = i[2]


#    out = defaultdict(list)

#    print dep
#    print par
#    print wtoi
#    print top
#    for i in xrange(len(dep)):
#        out[par[i]].append(words[i])
#    for x in out:
#        print out[x]

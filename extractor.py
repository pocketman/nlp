''' Answer Extractor Module'''

import api
import pygraphviz as pgv
import math

#edges
OBJ = ['prep_to', 'dobj', 'xcomp']

#general prohibited edges
GPE = ['appos', 'ccomp', 'xcomp', 'xconj', 'conj', 'conj_negcc']

#prohibited edges
OBJPE = ['nsubj', 'cop']
OBJPE.extend(GPE)

#transforms sentence into dependency graph
def getGraph(s):
    G = {}
    orig = api.toString(s)
    dep = api.corenlp.raw_parse(orig)['sentences'][0]['indexeddependencies']
    for d in dep:
        #rel(x,y) gives the relation of y to x
        #interpret it as y is a rel(x,y) of x
        rel = d[0] #relationship between words
        x = d[1] # the word that y is in relation to
        y = d[2] # the word that we want to find the relation of

        if not y in G:
           G[y] = []
        if x in G:
            if (y, rel) in G[x]:
                continue
            else:
                G[x].append((y,rel))
        else:
            G[x] = [(y,rel)]
    return G
#s is the string you want to turn into a graph
def visualizeGraph(s):
    p = api.parseS(s)
    G = getGraph(p[0])
    vis = pgv.AGraph(directed=True)
    vis.graph_attr['label'] = api.toString(p[0])
    for v in G:
        vis.add_node(v)
    for v in G:
        for tpl in G[v]:
            vis.add_edge(v, tpl[0], label=tpl[1])
    vis.draw('graph.png', prog='circo')


#returns the index of the string node
def idx(node):
    itms = node.split('-')
    return int(itms[1])-1

#returns the word of a string node
def word(node):
    itms = node.split('-')
    return itms[0]

#The function finds all nodes which have a t typed edge
#G is the graph
#curr is the current node
#t is a string representing the relation your looking for
#visited is a dict of visited nodes
def gSearch(G, curr, t, visited, results):
    visited[curr] = True
    for nb in G[curr]:
        w = nb[0]
        tp = nb[1]
        if w in visited:
            continue
        if tp == t:
            if not curr in results:
                results.append(curr)
        (visited, results) = gSearch(G, w, t, visited,results)
    return (visited, results)
#searches for a word instead of a type
def wSearch(G, curr, target, visited,results):
    visited[curr] = True
    for nb in G[curr]:
        w = nb[0]
        tp = nb[1]
        if w in visited:
            continue
        if target == word(w):
            if not curr in results:
                results.append(curr)
        (visited, results) = gSearch(G, w, target, visited,results)
    return (visited, results)

def gSearchW(G, start, t):
    visited = {}
    (junk, result) = gSearch(G, start, t, visited,[])
    return result
def wSearchW(G, start, w):
    visited = {}
    (junk, result) = wSearch(G,start,w,visited, [])
    return result

#extracts subj/verb/obj of a question
#s is the question, t is question type
def getQ(t,s):
    subj = None
    vb = None
    obj = None
    G = getGraph(s)
    pnodes = gSearchW(G, 'ROOT-0', 'aux') # look for primary node with an aux edge
    if t == 0:
        if len(pnodes)==0:
            pnodes = gSearchW(G, 'ROOT-0', 'cop')
        if len(pnodes)==0:
            print 'Could not decipher question: ' + api.toString(s)
            return None
        pnode = pnodes[0]
        if 'VB' in s[idx(pnode)]['POS']:
            vb = word(pnode)
        elif 'NN' in s[idx(pnode)]['POS']:
            obj = getPhrase(G,pnode, OBJPE)
        for nb in G[pnode]:
            w = nb[0]
            rel = nb[1]
            if rel == 'nsubj':
                subj = getPhrase(G,w,GPE)
            elif not vb and rel == 'cop':
                vb = word(w)
            elif not obj and rel in OBJ:
                obj = getPhrase(G,w, GPE)
    else:
        print 'not yet implemented'
    return (subj, vb, obj)

#PE is prohibited edges that we don't want to traverse
#TODO get the prepositions too
def xtractPhrase(G, curr, visited, PE):
    visited.append(curr)
    for nb in G[curr]:
        node = nb[0]
        if node in visited or nb[1] in PE:
            continue
        visited = xtractPhrase(G, node, visited,PE)
    return visited
        
def getPhrase(G, w, PE):
    visited = []
    stack = xtractPhrase(G,w, visited, PE)
    stack = map(lambda x: (word(x),idx(x)),stack)
    stack = sorted(stack, key=lambda e: e[1])
    stack = map(lambda x: x[0], stack)
    phrase = ' '.join(stack)
    return phrase

#define answers
#-1 negative, 0 don't know, 1 positive
def getYN(svo, s):
    G = getGraph(s)
    subj = svo[0]
    vb = svo[1]
    obj = svo[2]
    subjects = gSearchW(G, 'ROOT-0', 'nsubj')
    subject = None
    pnode = None
    mindist = 100000
    #get the most similar subject
    for node in subjects:
        asubj = getPhrase(G,getSubj(G,node),GPE)
        if not asubj:
            continue
        newdist = phraseDist(subj,asubj)
        if newdist<mindist:
            subject = asubj
            pnode = node
            mindist = newdist
    if not pnode:
        return ANS[1] #don't know the answer
    #two cases, the sentence is an is or the sentence is a verb

    tok = s[idx(pnode)]

    #case 2
    if 'VB' in tok['POS']:
        if tok['word'] in svo[1]:
            if not svo[2]:
                return 1
            else:
                for neighbor in G[pnode]:
                    if neighbor[0] == subject:
                        continue
                    else:
                        p2 = getPhrase(G, neighbor[0], GPE)
                        if phraseDist(svo[2], p2)<0:
                            return 1
                return 0 
        else:
            return 0
    #case 1
    else:
        cop = False
        for neighbor in G[pnode]:
            if 'cop' in neighbor[1]:
                cop = True
        if cop:
            p2 = getPhrase(G, pnode, OBJPE)
            if phraseDist(svo[2], p2)<0:
                return 1
            else:
                return 0
        return 0
        

        

#returns similarity between two phrases
#really bad, needs to be smarter
AR = ['the', 'a', 'an']
def phraseDist(p1,p2):
    val = 0
    toks = p1.split(' ')
    for t in toks:
        if t in p2 and t not in AR:
            val-=1
    return val
#returns subject of a node with a subject
def getSubj(G, n):
    for nb in G[n]:
        w = nb[0]
        rel = nb[1]
        if 'subj' in rel:
            return w

'''    
def getNP():
def getT():
def getPer():
def getPlc():
'''

'''
This module deals with i/o of our input
'''

#returns a tuple of our questions (dict with key being qns_id)
def readQuestions(q_loc):
    labels = []
    qs = {}
    with open(q_loc) as file:
        labels = map(lambda x: x.strip(),file.readline().split("\t"))
        for line in file:
            question = {}
            tokens = map(lambda x: x.strip(), line.split("\t"))
            id = 0
            for i in xrange(len(tokens)):
                if labels[i]=='qns_id':
                    id = int(tokens[i])
                    continue
                question[labels[i]]=tokens[i]
            qs[id]=question
    return qs


    

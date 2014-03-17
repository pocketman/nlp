#encapsule all the info about the word in this class
class Word:

	def __init__(self):
		self.ner = None 
		self.pos = None
		self.lemma = None
		self.index = -1

	def setValue(ner, pos, lemma, index):
		self.ner = ner
		self.pos = pos
		self.lemma = lemma
		self.index = -1


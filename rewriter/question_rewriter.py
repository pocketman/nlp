import utils
from rewriter_utils import RewriterUtils

class QuestionRewriter:

	@staticmethod
	def getTheIndexOfVBZ(wordList, POSMap):
		for i in xrange(len(wordList)):
			if POSMap[wordList[i]] == 'VBZ' or POSMap[wordList[i]] == 'VBP':
				return i
		return -1

	@staticmethod
	#rewrite a list of words that are tokenized from the question
	def rewriteQuestion(inputSentence, addWHword = False):
		utils = RewriterUtils()
		utils.parse(inputSentence)
		vbzIndex = QuestionRewriter.getTheIndexOfVBZ(utils.wordList, utils.posMap)
		if vbzIndex == -1:
			raise Exception("No VBZ found!")

		rewrittenQuestion = [] 
		for i in xrange(vbzIndex + 1, len(utils.wordList)):
			rewriteQuestion.append(util.wordList[i])
		if addWHword:
			rewrittenQuestion.append(utils.wordList[vbzIndex])
		for i in xrange(0, vbzIndex):
			rewrittenQuestion.append(utils.wordList[i])
		return rewrittenQuestion

	
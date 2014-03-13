import utils
from rewriter_utils import RewriterUtils

class QuestionRewriter:

	@staticmethod
	def getTheIndexOfVBZ(wordList, POSMap):
		for i in xrange(len(wordList)):
			if POSMap[wordList[i]] == 'VBZ':
				return i
		return -1

	@staticmethod
	def rewriteQuestion(inputSentence):
		utils = RewriterUtils()
		utils.parse(inputSentence)
		vbzIndex = QuestionRewriter.getTheIndexOfVBZ(utils.wordList, utils.posMap)
		if vbzIndex == -1:
			raise Exception("No VBZ found!")

		rewrittenQuestion = ""
		for i in xrange(vbzIndex + 1, len(utils.wordList)):
			rewrittenQuestion += utils.wordList[i]
		rewrittenQuestion += utils.wordList[vbzIndex]
		for i in xrange(0, vbzIndex):
			rewrittenQuestion += utils.wordList[i]
		return rewrittenQuestion

	
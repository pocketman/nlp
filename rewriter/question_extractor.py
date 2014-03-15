import sys
sys.path.add("..")
import api
from rewriter_utils import RewriterUtils


class QuestionExtractor:

    @static method
    def simplifySentence(inputSentence):
        utils = RewriterUtils()
        utils.parse(inputSentence)
        #follow the path nsubj, dobj
        
        

	
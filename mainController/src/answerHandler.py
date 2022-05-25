
class AnswerHandler:
    # class variables
    _WRONG_ANSWER_LIMIT = 5
    _CLUE_LIMIT = 3
    def __init__(self,  currentAnswer = "", expectedAnswers = [], wrongAnswerCount=0):
        self.wrongAnswerCount = 0
        self.currentAnswer = currentAnswer
        self.expectedAnswers = expectedAnswers 

    def setCurrentAnswer(self, answer):
        self.currentAnswer = answer.lower()
        
    def incrementWrongAnswerCount(self):
        if(self.wrongAnswerCount + 1 > AnswerHandler._WRONG_ANSWER_LIMIT):
            return -1
        self.wrongAnswerCount+=1

    def resetWrongAnswerCount(self):
        self.wrongAnswerCount = 0

    def isWrongAnswerLimitReached(self):
        return self.wrongAnswerCount >= AnswerHandler._WRONG_ANSWER_LIMIT
    def isClueNeeded(self):
        return self._CLUE_LIMIT == self.wrongAnswerCount

    def setExpectedAnswers(self, answers):
        # save as uppercase answers
        self.expectedAnswers = [a.lower() for a in answers]
    
    def isCorrectAnswer(self):
        if(self.currentAnswer is None or len(self.currentAnswer) == 0): 
            return -1
        if self.currentAnswer in self.expectedAnswers:
            return True
        else:
            return False

import ast
import json

class QuestionHandler:
    def __init__(self,  currentQuestion = "",  expectedAnswers = [], currentLevel=0, currentFallbackLevel = 0, isLastQuestion = False):
        self.currentQuestion = currentQuestion
        self.expectedAnswers = expectedAnswers
        self.currentLevel = currentLevel
        self.currentFallbackLevel = currentFallbackLevel
        self.isLastQuestion = isLastQuestion 

    def setCurrentQuestion(self, question):
        self.currentQuestion =  question 

    def setExpectedAnswers(self, answers):
        self.expectedAnswers= answers
    
    def setCurrentLevel(self, level):
        self.currentLevel = level

    def setCurrentFallbackLevel(self, fallbackLevel):
        self.currentFallbackLevel = fallbackLevel

    
    def getQuestionList(self):
        with open('src/questions.json') as f:
            data = json.load(f)
        return data["questions"]

    def getClue(self,questions,  level, fallbackLevel):
        if(fallbackLevel == 0):
            return questions[level]["clue"]
        return questions[level]["fallbacks"][fallbackLevel - 1]["clue"]

    def upgradeLevel(self, level, fallbackLevel, question, answer,  questions):
        level=level+1
        fallbackLevel = 0
        answer.resetWrongAnswerCount()
        if(level >= len(questions)):
            print("All Levels Completed")
            self.isLastQuestion = True
            return 0,0
        question.setCurrentQuestion(questions[level]["question"])
        question.setCurrentLevel(level)
        question.setCurrentFallbackLevel(fallbackLevel)
        correctAnswers = questions[level]["expectedAnswers"]
        question.setExpectedAnswers(correctAnswers)
        answer.setExpectedAnswers(correctAnswers)
        tempLevel=level+1
        print("upgraded to level: %d" % tempLevel)
        return level, fallbackLevel
    def fallback(self, level, fallbackLevel, question, answer,  questions):
        level=level
        fallbackLevel = fallbackLevel + 1
        fallbackQuestions = questions[level]["fallbacks"]
        # answer.resetWrongAnswerCount()

        if(fallbackLevel >= len(fallbackQuestions)):
            print("fallback limit reached")
            
            return self.upgradeLevel(level, fallbackLevel, question, answer,  questions)

        question.setCurrentQuestion(fallbackQuestions[fallbackLevel - 1]["question"])
        question.setCurrentLevel(level)
        question.setCurrentFallbackLevel(fallbackLevel)
        correctAnswers = fallbackQuestions[fallbackLevel - 1]["expectedAnswers"]
        question.setExpectedAnswers(correctAnswers)
        answer.setExpectedAnswers(correctAnswers)
        tempLevel=level+1
        print("fallen back to Level:  %d  FallbackLevel: %d " % (tempLevel, fallbackLevel))
        return level, fallbackLevel

    def printAndPublishQuestion(self, questions, level, fallbackLevel, textToSpeechQueue):
        if(fallbackLevel == 0):
            q = questions[level]["question"]
            print(q)
            textToSpeechQueue.publish(payload=q)
        else:
            q = questions[level]["fallbacks"][fallbackLevel - 1]["question"]
            print(q)
            textToSpeechQueue.publish(payload=q)

    def printAndPublishDescription(self, questions, level, fallbackLevel, textToSpeechQueue):
        if(fallbackLevel != 0):
            return
        else:
            des = questions[level]["description"]
            print(des)
            textToSpeechQueue.publish(payload=des)
    

# if __name__ == "__main__":
#     questionHandler = QuestionHandler()
#     data = questionHandler.getQuestionList()
#     print(data)

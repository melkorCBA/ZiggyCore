
class Person:
    def __init__(self, name="Cba", faceId=None, score=0, wrongAnswers=[], emotions = [] ,  currentEmotion="") -> None:
        self._name = name
        self._faceId = faceId
        self._score = score
        self._wrongAnswers = wrongAnswers
        self._emotions = emotions
        self._currentEmotion = currentEmotion

    def setCurrentPerson(self, name, faceId):
        self._name = name
        self._faceId = faceId
        self._score = 0

    def updateScore(self, inc=0, dec=0, wrongAnswer=None, overwright=None):
        # wrongAnswer={"level":-1, "fallbackLevel": -1}
        if (overwright is not None):
            self._score = overwright
            return
        if(wrongAnswer is not None):
            self._wrongAnswers.append(wrongAnswer)
        self._score = self._score  + inc - dec

    def getScore(self):
        return self._score

    def getName(self):
        return self._name

    def isNewPerson(self, currentFrameFaceId, currentFaceName):
        if(self._faceId != currentFrameFaceId):
            print("NEW PERSON (%s) DETECTED" % currentFaceName)
            self._name = None
            self._faceId = None
            self._score = 0
            self._wrongAnswers = []
            return True
        return False
    def printResults(self):
        correctAnswersCount = self._score / 5
        wrongAnsersCount = len(self._wrongAnswers)
        
        print("----------------------------------------------------------------")
        print("                     Performance Scores                         ")
        print("----------------------------------------------------------------")
        print("name :%s total score: %d c-ans-count: %d w-ans-count %d " % (self._name, self._score, correctAnswersCount, wrongAnsersCount))
        print("----------------------------------------------------------------")
        print("                   Wrong Answers Deatails                       ")
        print("----------------------------------------------------------------")
        for wrAns in self._wrongAnswers:
            print("            Level : %d        Fallbacl Level: %d                " % (wrAns["level"], wrAns["fallbackLevel"]))

    def _addEmotion(self, emotion):
        if(len(self._emotions) == 3):
            del self._emotions[2]
            self._emotions.insert(0, emotion)
        else:
            self._emotions.insert(0, emotion)
    def setCurrentEmotion(self, emotion):
        self._currentEmotion = emotion
        self._addEmotion(self._currentEmotion)

    def isInHappyOrNutralState(self):
        if(len(self._emotions) != 3):
           return True
        if(self._currentEmotion !=  "angry" and self._currentEmotion != "disguest" and self._currentEmotion != "fear" and self._currentEmotion != "sad"):
            return True
        previousStates = self._emotions[-2:]
        if(self._currentEmotion in previousStates):
            return False
        return True
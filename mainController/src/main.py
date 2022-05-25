from  multipleQueue import RabbitMqServerConfigure, rabbitmqServer
from questionHandler import QuestionHandler
from answerHandler import AnswerHandler
from queueSender import RabbitMqConfigureSender , RabbitMqSender
import json
import time
from person import Person


Queues = [{"name": "speech-to-text", "routingKey": "speech"},  {"name": "face-info", "routingKey": "face"}, {"name": "text-to-speech-status", "routingKey": "tts-status"}]
question = QuestionHandler()
questions = question.getQuestionList()


STATUS = 0 # 0 - not started, 1 - ongoing 
answer = AnswerHandler()
currentPerson = Person()
CURRENT_LEVEL = 0
CURRENT_FALLBACK_LEVEL = 0
CurrentEmotion = ""

#tts speaker status
isTTSInSpeechSataus = False


def getTextToSpeechQueueSender():
    textToSpeechServer = RabbitMqConfigureSender(queue='text-to-speech', host='localhost', routingKey='text', exchange='main-exchnage')
    # initlize  test-to-speech queue senders
    return RabbitMqSender(textToSpeechServer)

def getMotorActionQueueSender():
    motorActionServer = RabbitMqConfigureSender(queue='motor-action', host='localhost', routingKey='m-action', exchange='main-exchnage')
    # initlize  motor action queue senders
    return RabbitMqSender(motorActionServer)


def addTextToTextToSpeechQueue(text):
    getTextToSpeechQueueSender().publish(payload=text)


def inilizer():
    global CURRENT_LEVEL
    global CURRENT_FALLBACK_LEVEL
    CURRENT_LEVEL = 0
    CURRENT_FALLBACK_LEVEL = 0
    addTextToTextToSpeechQueue("Hello %s! I am Zig,Teaching Assistant Robot. Let's learn some English." % currentPerson.getName())
    time.sleep(1)
    question.setCurrentQuestion(questions[CURRENT_LEVEL]["question"])
    question.setCurrentLevel(CURRENT_LEVEL)
    question.setCurrentFallbackLevel(CURRENT_FALLBACK_LEVEL)
    correctAnswers = questions[CURRENT_LEVEL]["expectedAnswers"]
    question.setExpectedAnswers(correctAnswers)
    answer.setExpectedAnswers(correctAnswers)
    # send description to queue
    question.printAndPublishDescription(questions, CURRENT_LEVEL, CURRENT_FALLBACK_LEVEL, getTextToSpeechQueueSender())
    time.sleep(5)
    # send question  to queue
    question.printAndPublishQuestion(questions, CURRENT_LEVEL, CURRENT_FALLBACK_LEVEL, getTextToSpeechQueueSender())
    

def generelCallback(ch,method, properties, body):
    routingKey = method.routing_key
    if(routingKey == "speech"):
        speechToTextCallback(ch,method, properties, body)
    if(routingKey == "face"):
        faceInfoCallback(ch,method, properties, body)
    if(routingKey == "tts-status"):
        ttsStateCallback(ch,method, properties, body)
    

def faceInfoCallback(ch,method, properties, body):
    global STATUS
    print("face update")
    data = json.loads(body)
    emotion = data["emotion"]
    name = data["person"]
    faceId = data["faceID"]
    if(currentPerson.isNewPerson(faceId, name)):
        currentPerson.setCurrentPerson(name, faceId)
        STATUS = 0
        return
    currentPerson.setCurrentPerson(name, faceId)
    # reset person and halut the ativity
    
    global CurrentEmotion
    currentPerson.setCurrentEmotion(emotion)

    if(not currentPerson.isInHappyOrNutralState()):
        CurrentEmotion = emotion
        addTextToTextToSpeechQueue("Don't give up %s." % currentPerson.getName())
        sendMotorActionToQueue('special')
    

def speechToTextCallback(ch,method, properties, body):
    global STATUS
    global CURRENT_LEVEL
    global CURRENT_FALLBACK_LEVEL
    global isTTSInSpeechSataus
    # doesn't expect any transcripts while robot is talking
    if(isTTSInSpeechSataus):
        return
    print('spoke')
    
    data = json.loads(body)
    word = data["word"]
    # print(word)
    if(word != ""):
        word = " ".join(word.split())
        
        if(question.isLastQuestion):
            return

        # greet and start/init
        if(word.lower() == "hello ziggy" and STATUS == 0):
            STATUS = 1
            inilizer()
            return
        if(STATUS != 1): return # check program is started  
        answer.setCurrentAnswer(word)
        if(answer.isCorrectAnswer() != -1 and answer.isCorrectAnswer()):
            print("CORRECT ANSWER")
            currentPerson.updateScore(inc=5)
            addTextToTextToSpeechQueue("Yes!" + word +" is correct.")
            sendMotorActionToQueue("yes")
            time.sleep(3)
            addTextToTextToSpeechQueue("Let's move to next section.")
            # go to next level diffculty
            CURRENT_LEVEL, CURRENT_FALLBACK_LEVEL = question.upgradeLevel(CURRENT_LEVEL, CURRENT_FALLBACK_LEVEL, question, answer, questions)
            # check if all levels completed
            if(question.isLastQuestion):
                addTextToTextToSpeechQueue("Hi %s. This is the end of the lesson. Thank you! Will meet again with the next lesson" % currentPerson.getName())
                currentPerson.printResults()
                return
            
            # send description to queue
            question.printAndPublishDescription(questions, CURRENT_LEVEL, CURRENT_FALLBACK_LEVEL, getTextToSpeechQueueSender())
            time.sleep(5)
            # send question  to queue
            question.printAndPublishQuestion(questions, CURRENT_LEVEL, CURRENT_FALLBACK_LEVEL, getTextToSpeechQueueSender())
        elif(answer.isCorrectAnswer() != -1 and not answer.isCorrectAnswer()):
            
            if(not answer.isWrongAnswerLimitReached()):
                answer.incrementWrongAnswerCount()
                print("WRONG ANSWER")
                currentPerson.updateScore(wrongAnswer={"level": CURRENT_LEVEL, "fallbackLevel": CURRENT_FALLBACK_LEVEL})
                addTextToTextToSpeechQueue("Sorry, answer is not " + word +".")
                sendMotorActionToQueue("no")
                if( answer.isClueNeeded()):
                    print("GIVING A CLUE")
                    addTextToTextToSpeechQueue("Here is a clue for you. " + question.getClue(questions, CURRENT_LEVEL, CURRENT_FALLBACK_LEVEL) +".")
                return
            print("WRONG ANSWER LIMIT REACHED !!")
            addTextToTextToSpeechQueue("Sorry, answer is not " + word +".")
            time.sleep(3)
            addTextToTextToSpeechQueue("Anyway, let's move to next section.")
             # go to fallback question
            CURRENT_FALLBACK_LEVEL = 0
            CURRENT_LEVEL, CURRENT_FALLBACK_LEVEL = question.fallback(CURRENT_LEVEL, CURRENT_FALLBACK_LEVEL, question, answer, questions)
            question.printAndPublishQuestion(questions, CURRENT_LEVEL, CURRENT_FALLBACK_LEVEL, getTextToSpeechQueueSender())

def ttsStateCallback(ch,method, properties, body):
    global isTTSInSpeechSataus
    data = json.loads(body)
    state = data["isSpeechState"]
    print('tts inSpeechState update to %r' % state)
    isTTSInSpeechSataus = state


def main():


    # callbacks
    # callbacks.append(spokeCallback)
    # callbacks.append(speakCallback)
    Callback = generelCallback

    # text tot speech consumer
    ChannelConfig = RabbitMqServerConfigure(host='localhost',  queues= Queues,  exchange='main-exchnage')
    queueChannel = rabbitmqServer(server=ChannelConfig)                                       
    queueChannel.subscribeQueue(Callback)

def sendMotorActionToQueue(action):
    getMotorActionQueueSender().publish(payload={"expression": action})

main()
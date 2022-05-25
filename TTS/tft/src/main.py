from queueReciver import RabbitMqServerConfigure, rabbitmqServer
from textToSpeech import ConfigureSpeechEngine
import json
from queueSender import RabbitMqConfigureSender, RabbitMqSender

# initlize state queues
ttsStatusServer = RabbitMqConfigureSender(queue='text-to-speech-status', host='localhost', routingKey='tts-status', exchange='main-exchnage')
speechEngine = ConfigureSpeechEngine(stateQueueConfig=ttsStatusServer)




def main():
    
    serverconfigure = RabbitMqServerConfigure(host='localhost', queue='text-to-speech',  routingKey='text',  exchange='main-exchnage')
    server = rabbitmqServer(server=serverconfigure)
    server.subscribeQueue(textToSpeechQueueCallBack)
    print("speaker is idle..")

def summaryText(text):
    len(text) > 0
    ln = len(text) // 4
    return "message recived: " + text[0: ln] + "...."

def textToSpeechQueueCallBack(text):
    # set to speech state
    speechEngine.sendState(isSpeechSate=True)
    print(summaryText(text.decode("utf-8") ))
    speechEngine.Speak(text.decode("utf-8") )

main()
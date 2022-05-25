from gtts import gTTS
from io import BytesIO
import os 
from playsound import playsound
from halo import Halo
from queueSender import  RabbitMqSender
import time


class ConfigureSpeechEngine:
    def __init__(self, language='en', slow=False, stateQueueConfig=None):
        self.language = language
        self.slow = slow
        self.stateQueueConfig = stateQueueConfig
        
    def convertToSpeech(self, text):
        return  gTTS(text=text, lang=self.language, slow=self.slow)
    

    def Speak(self, text):
        spinner = None
        if(text != '' or text != ' '):
            tts = self.convertToSpeech(text)
            spinner = Halo(spinner='line')
            tts.save('aud.mp3')
            spinner = None
            print("talking: %s" % text)
            playsound('aud.mp3')
            os.remove('aud.mp3')
            time.sleep(3)
            # set to idel state
            self.sendState(False)
            print("speaker is idle..")
               
    def sendState(self, isSpeechSate = False):
        ttsStatusQueue =  RabbitMqSender(self.stateQueueConfig)
        ttsStatusQueue.publish(payload={"isSpeechState": isSpeechSate})
# if __name__ == "__main__":
   
#     engin = ConfigureSpeechEngine()
#     engin.Speak("his wikiHow teaches you how to install FFmpeg onto your Windows 10 computer. FFmpeg is a command line-only program that allows you to convert videos and audio into different formats, as well as record live audio and video.")
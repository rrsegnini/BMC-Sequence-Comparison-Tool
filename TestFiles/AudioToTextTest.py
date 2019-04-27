import speech_recognition as sr
import Main as M
import LyricsTest as lt
#Fuente: https://pypi.org/project/SpeechRecognition/

# obtain path to "english.wav" in the same folder as this script
from os import path
AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "hola.wav")
AUDIO_FILE_2 = path.join(path.dirname(path.realpath(__file__)), "siboney.wav")
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "chinese.flac")

# use the audio file as the audio source
r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source) # read the entire audio file
    #print("Pruebas audios 0")
    #print(audio.frame_data)

with sr.AudioFile(AUDIO_FILE_2) as source:
    audio2 = r.record(source) # read the entire audio file
    #print("Prueba audios")
    #print(audio.frame_data)

print(M.NeedlemanWunsch(lt.get_lyrics("David Bowie","Ziggy Stardust")[0:12],lt.get_lyrics("Roger Waters","Déjà Vu")[0:12],1,-1,-2))

#print(audio.frame_data)
#print(audio2.frame_data)

# recognize speech using Google Speech Recognition
try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

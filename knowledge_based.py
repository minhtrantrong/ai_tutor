import os
import pyttsx3 as tts

# Create a text to speech engine
engine = tts.init()
voices = engine.getProperty('voices')       #getting details of current voice
#engine.setProperty('voice', voices[0].id)  #changing index, changes voices. 0 for male
engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female

def SpeakText(text): 
    engine.say(text)
    engine.runAndWait()
    return
    
def read(lecture_file, keys=["[LECTURE]", "[IMAGE]", "[Q&A]", "[END]"]):
    # lecture_file is a plain text file (.txt)
    # kb is a knowledge based in dictionary data type
    kb = {}
    with open(lecture_file, 'r') as lf:
        lecture = lf.readlines()
        doc_len = len(lecture)
        index = 0
        keys_index = []
        while index < doc_len:
            line = lecture[index]
            line = line.strip()
            if len(line) == 0:
                continue
            if line[0] =="#":
                continue
            if line in keys:
                keys_index.append(index)

            index += 1
        for i in range(len(keys_index)):
            idx = keys_index[i]
            key = lecture[idx]
            if key != "[END]":
                next_idx = keys_index[i+1]
                kb[key] = tuple(lecture[idx+1: next_idx])
    return kb
                


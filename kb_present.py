import os
from PIL import Image, ImageTk
import tkinter as tk
from datetime import datetime
import pyttsx3 as tts
import time

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
lectures_dir = os.path.join(current_dir, "lectures")
save_dir = os.path.join(parent_dir, "saved_data")



# Create a text to speech engine
engine = tts.init()
voices = engine.getProperty('voices')       #getting details of current voice
#engine.setProperty('voice', voices[0].id)  #changing index, changes voices. 0 for male
engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female
engine.setProperty('rate', 125)

#-------------------------------------------------------------------------------------------------#
def SpeakText(text): 
    engine.say(text)
    engine.runAndWait()
    return
#-------------------------------------------------------------------------------------------------#
def read_lectures(lecture_file, keys=["[LECTURE]", "[IMAGE]", "[Q&A]", "[END]"]):
    # lecture_file is a plain text file (.txt)
    # kb is a knowledge based in dictionary data type
    lecture = []
    with open(lecture_file, 'r') as lf:
        lines = lf.readlines()
        for line in lines:
            if len(line) == 0:    
                continue
            if line[0] =="#":
                continue
            lecture.append(line.strip())
        doc_len = len(lecture)
        print("Length of document: ", doc_len)
        index = 0
        keys_index = []
        while index < doc_len:
            line = lecture[index]
            line = line.strip()
            line = line.strip("\n")
            
            if len(line) == 0:  
                index += 1   
                continue
            if line[0] =="#":
                index += 1
                continue
            if line in keys:
                keys_index.append(index)
            index += 1
            print("index: ", index)
        print("All key index: ", keys_index)
        
    return keys_index, lecture
                
#-------------------------------------------------------------------------------------------------#
def display_image(image_path, chat_window):
    print("display images on chat window")
    img = ImageTk.PhotoImage(Image.open(image_path))
    chat_window.image_create(tk.END, image = img) 
    return

#-------------------------------------------------------------------------------------------------#
def display_lecture(lecture, chat_window):
    # lecture is a list of sentences
    print("display lecture on chat window")
    chat_window.insert(tk.END, "TUTOR: " + '\n\n')
    for sentence in lecture:
        chat_window.insert(tk.END, sentence + '\n\n')
        time.sleep(1)
        SpeakText(sentence)
    return

#-------------------------------------------------------------------------------------------------#
def q_and_a(suggestion, chat_window):
    print("Start Q&A ...")
    # suggestion is a list of sentences
    chat_window.insert(tk.END, "TUTOR: " + '\n\n')
    for sentence in suggestion:
        chat_window.insert(tk.END, sentence + '\n\n')
        time.sleep(1)
        SpeakText(sentence)
    next_suggest = "If there are no questions, enter continue or next to finish"
    chat_window.insert(tk.END, next_suggest + '\n\n')
    SpeakText(next_suggest)
    return

#-------------------------------------------------------------------------------------------------#
def tutor(subject, chat_window):
    print("Start tutor fucntion")
    # subject is a string, name of course subject
    # chat_window is an object used to display knowledge
    subject_name = "_".join(subject.split()) 
    subject_file = subject_name + ".txt"
    subject_dir = os.path.join(lectures_dir, subject_name)
    images_dir = os.path.join(subject_dir, "images")
    subject_file_path = os.path.join(subject_dir, subject_file)
    # Read the lectures file
    print("Start reading the lecture")
    keys_index, lectures = read_lectures(subject_file_path, keys=["[LECTURE]", "[IMAGE]", "[Q&A]", "[END]"])
    for i in range(len(keys_index)):
        idx = keys_index[i]
        print("idx: ", idx)
        key = lectures[idx].strip()
        key = key.strip("\n")

        if key != "[END]":
            next_idx = keys_index[i+1]
            lecture = lectures[idx+1: next_idx]
        print("KEY: ", key)
        print("LECTURE: ", lecture)
        #print(key == "[LECTURE]")
        if key == "[LECTURE]":
            print("Display lecture")
            display_lecture(lecture, chat_window)
        if key == "[IMAGE]": 
            print("Display images")
            for img_file in lecture:
                img_file = img_file.strip()
                if img_file == "":
                    continue
                if img_file[0] == "#":
                    continue
                
                img_path = os.path.join(images_dir, img_file)
                display_image(img_path, chat_window)
        if key == "[Q&A]":
            print("Display Q&A")    
            q_and_a(lecture, chat_window)
    return

#-------------------------------------------------------------------------------------------------#
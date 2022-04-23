import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
import kb_present

from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))

nltk.download('omw-1.4')

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res


#Creating GUI with tkinter
import tkinter
from tkinter import *


def send():
    msg = chat_box.get("1.0",'end-1c').strip()
    chat_box.delete("0.0",END)
    res = ""
    if msg != '':
        chat_window.config(state=NORMAL)
        chat_window.insert(END, "You: " + msg + '\n\n')
        chat_window.config(foreground="#442265", font=("Verdana", 12 ))
    
        res = chatbot_response(msg).lower()
        load_kb = (res.split("::")[0].strip() == "loading knowledge")
        
        if not load_kb:
            chat_window.insert(END, "Tutor: " + res + '\n\n')
            kb_present.SpeakText(res)
            
        else:
            subject = res.split("::")[1]
            tutor_res = "Alright, please wait for loading knowledge"
            chat_window.insert(END, "TUTOR: " + tutor_res + '\n\n')
            kb_present.tutor(subject, chat_window)
        chat_window.config(state=DISABLED)
        chat_window.yview(END)
    return

window = Tk()
window.title("AI TUTOR")
window.geometry("800x500")
window.resizable(width=True, height=True)
window.grid_columnconfigure((0,1,2,3), uniform="uniform", weight=1)
window.grid_rowconfigure(0, weight=1)
# Create frame
frame = Frame(window).grid(row=0, column=1, columnspan=3, sticky=NSEW)
#Create Chat window
chat_window = Text(frame, bd=0, bg="white", height="8", width="50", font="Arial")
#chat_window.pack(fill="both", expand=True)
chat_window.config(state=DISABLED)

#Bind scrollbar to Chat window
scrollbar = Scrollbar(window, command=chat_window.yview, cursor="heart")
chat_window['yscrollcommand'] = scrollbar.set

#Create Button to send message
SendButton = Button(window, font=("Verdana",12,'bold'), text="Send", width="12", height=5,
                    bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',
                    command=send)

#Create the box to enter message
chat_box = Text(frame, bd=0, bg="white",width="29", height="5", font="Arial")
#chat_box.pack(fill="both",expand=True)
chat_box.bind("<Return>", send())


#Place all components on the screen
scrollbar.place(x=776,y=6, height=386)
chat_window.place(x=6,y=6, height=386, width=770)
chat_box.place(x=128, y=401, height=90, width=665)
SendButton.place(x=6, y=401, height=90)

window.mainloop()

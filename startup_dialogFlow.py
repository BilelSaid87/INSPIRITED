import speech_recognition as sr
import pickle
import json
import time
import os
import tensorflow as tf
import numpy as np
import tflearn
import nltk
import random
from nltk.stem.snowball import SnowballStemmer
stemmer= SnowballStemmer('german')
#from nltk.stem.lancaster import LancasterStemmer
#stemmer = LancasterStemmer()


def main():
    THRESHOLD=0
    loadModel = True
    data = pickle.load(open("data/training_data", "rb"))
    words = data['words']
    classes = data['classes']
    train_x = data['train_x']
    train_y = data['train_y']
    with open('data/intents.json') as json_data:
        intents = json.load(json_data)
    if loadModel == True:
        # reset underlying graph data
        tf.reset_default_graph()
        # Build neural network
        net = tflearn.input_data(shape=[None, len(train_x[0])])
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
        net = tflearn.regression(net)
        # Define model and setup tensorboard
        model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
        model.load('trainedModels/therapieModelUsingBOW_tflearn')
    for i in range(333):
        #print('say something: ')
        #sentence = speechtotext()
        sentence=input('user says: ')
        response(sentence, intents, words, classes, model, THRESHOLD)
        print("classes", classes)
        time.sleep(1)


def response(sentence,intents, words, classes,model,THRESHOLD):
    results = classify(sentence, words, classes, model, THRESHOLD)
    print(results)
    # if we have a classification then find the matching intent tag
    if results:
        # loop as long as there are matches to process
        while results:
            for i in intents['intents']:
                # find a tag matching the first result
                if i['tag'] == results[0][0]:
                    # a random response from the intent
                    res = random.choice(i['responses'])
                    os.system('say '+res)
                    return print(res)
            results.pop(0)
    else:
        res = 'Tut mir Leid, ich habe Sie nicht richtig Verstanden'
        os.system('say ' + res)
        print(res)




def classify(sentence, words, classes, model, THRESHOLD):
    # generate probabilities from the model
    results = model.predict([bow(sentence, words, True, True)])[0]
    print("prob sum is", np.sum(results))
    # filter out predictions below a threshold
    results = [[i,r] for i,r in enumerate(results) if r>THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    # return tuple of intent and probability
    return return_list

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details, useStemmer):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence,useStemmer)
    # bag of words
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def clean_up_sentence(sentence, useStemmer):
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word
    if (useStemmer == True):
      sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

def speechtotext():
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)
    s = r.recognize_google(audio, language="de-DE")
    #s = r.recognize_sphinx(audio, language="en-US")
    try:
      print("SpeechToText: " + s)
    except sr.UnknownValueError:
      print("Audio input ist nicht verständlich")
    except sr.RequestError as e:
      print("Could not request results;{0}".format(e))
    return s

if __name__ == "__main__":
    main()
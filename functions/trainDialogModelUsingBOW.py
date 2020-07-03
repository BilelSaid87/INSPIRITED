import json
import numpy as np
import random
import tensorflow as tf
import tflearn
import pickle
from functions.common_utils import *
from nltk.stem.snowball import SnowballStemmer
stemmer= SnowballStemmer('german')


def main():
  # read json intents file
  with open('../data/intents.json') as jsonData:
      intents = json.load(jsonData)
  # extract patterns vocabulary
  classes, documents, sentences, words = getPatternsFromJson(intents, useStemmer=True)
  print(len(documents), "documents")
  print(len(classes), "classes", classes)
  print(len(words), "unique stemmed words")
  train_x, train_y = trainingDataBagOfWords(classes, documents, words)
  print("documents",documents)
  print("words",words)
  print("sentences",sentences)
  print("train_x",train_x)
  print("train_y", train_y)
  print("classes",classes)
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
  # Start training (apply gradient descent algorithm)
  model.fit(train_x, train_y, n_epoch=1000, batch_size=32, show_metric=True)
  model.save('../trainedModels/therapieModelUsingBOW_tflearn')
  pickle.dump({'words':words, 'classes':classes, 'train_x':train_x, 'train_y':train_y}, open("../data/training_data", "wb"))



def trainingDataBagOfWords(classes,documents,words):
    # create our training data
    training = []
    output = []
    # create an empty array for our output
    output_empty = [0] * len(classes)

    # training set, bag of words for each sentence
    for doc in documents:
      # initialize our bag of words
      bag = []
      # list of tokenized words for the pattern
      pattern_words = doc[0]
      # stem each word
      #pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
      # create our bag of words array
      for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

      # output is a '0' for each tag and '1' for current tag
      output_row = list(output_empty)
      output_row[classes.index(doc[1])] = 1
      training.append([bag, output_row])

    # shuffle our features and turn into np.array
    #random.shuffle(training)
    training = np.array(training)
    # create train and test lists
    train_x = list(training[:, 0])
    train_y = list(training[:, 1])
    return train_x, train_y


if __name__ == "__main__":
    main()
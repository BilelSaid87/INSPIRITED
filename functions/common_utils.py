import nltk
from nltk.stem.snowball import SnowballStemmer
stemmer= SnowballStemmer('german')


def getPatternsFromJson(intents,useStemmer):
  words = []
  classes = []
  documents = []
  sentences = []
  ignore_words = ['Ich','ich','?', '!', ',', '.']
  # loop through each sentence in our intents patterns
  for intent in intents['intents']:
    for pattern in intent['patterns']:
      # tokenize each word in the sentence
      w = nltk.word_tokenize(pattern)
      # lower all words and replace special german letters
      w = [word.lower() for word in w]
      w = [word.replace('ß', 'ss') for word in w]
      w = [word.replace('ü', 'ue') for word in w]
      w = [word.replace('ä', 'ae') for word in w]
      w = [word.replace('ö', 'oe') for word in w]
      # use stemmer if required
      if useStemmer == True:
        w = [stemmer.stem(word) for word in w if word not in ignore_words]
      # add to our words list
      words.extend(w)
      # add to documents in our corpus
      documents.append((w, intent['tag']))
      # add to our classes list
      if intent['tag'] not in classes:
        classes.append(intent['tag'])
  #remove duplicates
  words = sorted(list(set(words)))
  #classes = sorted(list(set(classes)))
  for doc in documents:
    sentences.append(doc[0])
  print("sentences in intent file are", sentences)
  return classes, documents, sentences, words
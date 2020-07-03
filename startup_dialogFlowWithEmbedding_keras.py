from keras.models import load_model
from functions.wordEmbedding import *
from functions.trainDialogModelUsingWordEmbedding import sentenceWords2indices
from functions.common_utils import getPatternsFromJson
import json

intentsDataPath = 'data/intents.json'
kerasModelPath = 'trainedModels/therapieModelUsingEmbedding_keras'

with open(intentsDataPath) as jsonData:
    intents = json.load(jsonData)
# extract patterns vocabulary from intents data
intents_classes, intents_documents, intents_sentences, intents_words = getPatternsFromJson(intents, useStemmer=True)
model = load_model(kerasModelPath)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# load embedding matrix
emb_matrix, emb_words, emb_word2idx, emb_idx2word = extractEmbeddingData(embeddingModelPath, isbinaryModel, useStemmer = True)
max_len = len(max(intents_sentences, key=len))
useStemmer = True
ignore_words = ['Ich','ich', '?', '!', ',', '.']
sentence = ''
while sentence != 'end':
   sentence = input('user says: ')
   sentence = sentence.lower().split()
   if (useStemmer == True):
       sentence = [stemmer.stem(w) for w in sentence if w not in ignore_words]
       sentece = [w.replace('ß', 'ss') for w in sentence]
       sentece = [w.replace('ü', 'ue') for w in sentece]
       sentece = [w.replace('ä', 'ae') for w in sentece]
       sentece = [w.replace('ö', 'oe') for w in sentece]
   sentence_indices = sentenceWords2indices([sentence], max_len, emb_word2idx)
   prob = model.predict(sentence_indices)
   results = [[i, r] for i, r in enumerate(prob[0])]
   results.sort(key=lambda x: x[1], reverse=True)
   sorted_classes=[]
   sorted_prob=[]
   for r in results:
       sorted_classes.append(intents_classes[r[0]])
       sorted_prob.append(r[1])
   print('predicted prob. vector sorted: ', sorted_prob)
   print('predicted classes sorted: ',sorted_classes)
   print('max prob = : ', np.max(prob), ' ; index of max prob idx = : ', np.argmax(prob))
   print('predicted intent class =: ', intents_classes[np.argmax(prob)])
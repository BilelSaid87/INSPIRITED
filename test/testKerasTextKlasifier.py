from numpy import array
from keras.preprocessing.text import one_hot
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.embeddings import Embedding
from keras.models import load_model
import json


trainModel=False
#define documents
docs = [ 'gut',
         'sehr gut',
         'Gut gemacht!',
         'Gute Arbeit',
         'Tolle Leistung',
         'Schöne Arbeit',
         'Hervorragend!',
         'Schwach',
         'sehr schlecht',
         'Schlechte Leistung!',
         'nicht gut',
         'schwache Arbeit',
         'hätte besser machen können.']
# define class labels
labels = array([1,1,1,1,1,1,1,0,0,0,0,0,0])
# tokenizer
t=Tokenizer()
t.fit_on_texts(docs)
encoded_tokens=t.texts_to_sequences(docs)
print(encoded_tokens)
# integer encode the documents
vocab_size = 20
#encoded_docs = [one_hot(d, vocab_size) for d in docs]
#print(encoded_docs)
# pad documents to a max length of 4 words
max_length = 4
padded_docs = pad_sequences(encoded_tokens, maxlen=max_length, padding='pre')
print(padded_docs)
if trainModel is True:
  # define the model
  model = Sequential()
  model.add(Embedding(vocab_size, 8, input_length=max_length))
  model.add(Flatten())
  model.add(Dense(8))
  model.add(Dense(8))
  model.add(Dense(1, activation='sigmoid'))
  # compile the model
  model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])
  # summarize the model
  print(model.summary())
  # fit the model
  model.fit(padded_docs, labels, epochs=100, verbose=0)
  # evaluate the model
  loss, accuracy = model.evaluate(padded_docs, labels, verbose=0)
  print('Accuracy: %f' % (accuracy*100))
  model.save('kerasKlassifierModel')

model = load_model('kerasKlassifierModel')
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])
test=['gut','das ist schlecht']
test_tokens=t.texts_to_sequences(test)
test_tokens_padded=pad_sequences(test_tokens, maxlen=max_length, padding='pre')
print(test_tokens_padded)
prob=model.predict_proba(test_tokens_padded)
print('estimated prob of  the input sentence " ', test, ' " is prob =', prob)

outputs=[layer.output for layer in model.layers]
print(outputs)
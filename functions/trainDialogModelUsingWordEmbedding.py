import json
from functions.wordEmbedding import *
from functions.common_utils import *
from keras.models import Model
from keras.layers.embeddings import Embedding
from keras.layers import Dense, Input, Dropout, LSTM, Bidirectional,Activation
from keras.optimizers import Adam, SGD
from nltk.stem.snowball import SnowballStemmer
from sklearn.model_selection import train_test_split
from tflearn.layers.embedding_ops import embedding
stemmer= SnowballStemmer('german')


def main():
    intentsDataPath = '../data/intents_test.json'
    # read json intents file
    with open(intentsDataPath) as jsonData:
        intents = json.load(jsonData)
    # extract patterns vocabulary from intents data
    intents_classes, intents_documents, intents_sentences, intents_words = getPatternsFromJson(intents, useStemmer=True)
    # some da ta statistics
    len_sentences = []
    max_len = len(max(intents_sentences, key=len))
    for sentence in intents_sentences:
        len_sentences.append(len(sentence))
    print("sentences lengths: ", len_sentences)
    print("sentences mean lengths: ", np.mean(len_sentences))
    print("sentences variance lengths: ", np.var(len_sentences))
    print("longest sentence has", max_len, " words")
    num_classes = len(intents_classes)
    # load word embedding data
    emb_matrix, emb_words, emb_word2idx, emb_idx2word = extractEmbeddingData('../'+embeddingModelPath, isbinaryModel, useStemmer=True)
    # create keras model
    model = prep_keras_model((max_len,), num_classes, emb_matrix)
    model.summary()
    #opt = Adam(lr=0.00005)
    opt = SGD(lr=0.00001)
    model.compile(optimizer=opt,loss='categorical_crossentropy', metrics=['accuracy'])
    # define training data and train model
    sentence_indices = sentenceWords2indices(intents_sentences, max_len, emb_word2idx)
    classes_oh = classes_onehot(intents_documents, intents_classes)
    print("length of hole-Dataset is l = ", len(intents_sentences))
    train_x, test_x, train_y, test_y = train_test_split(sentence_indices, classes_oh,test_size=0.1,random_state=1)
    #train_x,val_x,train_y,val_y=train_test_split(train_x,train_y,test_size=0.1,random_state=1)
    print("length of training-Dataset is l_train = ", len(train_x))
    #print("length of validation-Dataset is l_val = ", len(val_x))
    print("length of test-Dataset is l_test = ", len(test_x))
    print("train_x[23]=",train_x[23])
    print("train_y[23]=", train_y[23])
    #print("val_x[3]=", val_x[3])
    #print("val_y[3]=", val_y[3])
    print("test_x[3]=", test_x[3])
    print("test_y[3]=", test_y[3])
    n_epochs = 100
    n=0
    #for epoch in range(n_epochs):
    #   n = n+1
    #   print('epoch : ',n)
    model.fit(train_x, train_y, validation_split=0.1,epochs=n_epochs, batch_size=8, shuffle=True)
    #   loss,acc=model.evaluate(val_x,val_y,verbose=0)
    #   print('acc val =',acc)
    #   print('loss val =',loss)
    loss, acc = model.evaluate(test_x, test_y, verbose=0)
    print('acc test =', acc)
    print('loss test =', loss)
    model.save('../trainedModels/therapieModelUsingEmbedding_keras')


def sentenceWords2indices(sentences, max_len, emb_word2idx):
    m = len(sentences)
    n1 = 0
    n2 = 0
    sentence_indices=np.zeros((m,max_len))
    for i in range(m):
      j = 0
      for w in sentences[i]:
          if j >= max_len:
             break
          try:
             sentence_indices[i,j] = emb_word2idx[w]
             n1 = n1+1
          except:
             sentence_indices[i,j] = 0
             n2 = n2+1
          j = j+1
    print(((n1*100)/(n1+n2)), ' % of the dataset words have been found in the embedding Matrix')
    return sentence_indices


def embedding_layer(emb_matrix):
    # prepare embedding layer
    vocab_len = emb_matrix.shape[0]
    emb_dim = emb_matrix.shape[1]
    emb_layer = Embedding(vocab_len,emb_dim,trainable=False)
    emb_layer.build((None,))
    emb_layer.set_weights([emb_matrix])
    return emb_layer


def prep_keras_model(input_shape, num_classes, emb_matrix):
    # define sentence indices as Input layer
    sentence_indices = Input(shape=input_shape, dtype='int32')
    # create the embedding layer
    emb_layer=embedding_layer(emb_matrix)
    # propagate the input through the embedding layer
    embeddings=emb_layer(sentence_indices)
    # Propagate the embeddings through an LSTM layer with 128-dimensional hidden state
    #X = Bidirectional(LSTM(128, return_sequences=True))(embeddings)
    # Add dropout
    #X = Dropout(0.3)(X)
    # Propagate X trough another LSTM layer with 128-dimensional hidden state
    X = Bidirectional(LSTM(128*2, return_sequences=False))(embeddings)
    # Add dropout with a probability of 0.5
    X = Dropout(0.5)(X)
    # Propagate X through a Dense layer with softmax activation to get back a batch of "ichnum_classes"-dimensional vectors.
    #X = Flatten()(embeddings)
    X = Dense(num_classes, activation='softmax')(X)
    # Add a softmax activation
    X = Activation('softmax')(X)
    # Create Model instance which converts sentence_indices into X.
    model = Model(inputs=sentence_indices, outputs=X)
    return model


    






def classes_onehot(documents,classes):
    m=len(documents)
    classes_index = np.zeros((m),'int32')
    i = 0
    for doc in documents:
       classes_index[i]=classes.index(doc[1])
       i = i+1
    classes_oh = np.eye(len(classes))[classes_index.reshape(-1)]
    return classes_oh

if __name__ == "__main__":
    main()


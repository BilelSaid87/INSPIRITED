import os
import numpy as np
from gensim.models.keyedvectors import KeyedVectors
from nltk.stem.snowball import SnowballStemmer
stemmer= SnowballStemmer('german')
embeddingModelPath = 'trainedModels/germanEmbedding.model'
isbinaryModel = True

def main():
    emb_matrix, words, word2idx, idx2word= extractEmbeddingData(embeddingModelPath, isbinaryModel, useStemmer=True)
    print("length idx2word:", len(idx2word))
    print("length word2idx:",len(word2idx))
    print(emb_matrix[1,:])
    #pickle.dump({'words': words}, open("data/germanEmbedding_words", "wb"))


def extractEmbeddingData(embeddingModelPath, isbinaryModel, useStemmer):
    word_vectors_model = loadEmbeddingModel(embeddingModelPath, isbinaryModel)
    word2idx = {}
    idx2word = {}
    words = list(word_vectors_model.wv.vocab.keys())
    vocab_len = len(words)
    emb_dim = len(word_vectors_model.wv[words[0]])
    emb_matrix = np.zeros((vocab_len+1,emb_dim))
    if useStemmer == True:
        words_out = stemEmbeddingWords(words)
    else:
        words_out = words
    for i in range(len(words)):
        word2idx.update({words_out[i]: i+1})
        idx2word.update({i+1: words_out[i]})
    idx=1
    for w in words:
        emb_matrix[idx,:] = word_vectors_model.wv[w]
        idx = idx+1
    print("Embedding Vocabulary size is: ", vocab_len)
    print("Word vector length is: ", emb_dim)
    print("Embedding Matrix created, dimension is: ", emb_matrix.shape)
    return emb_matrix, words_out, word2idx, idx2word


def loadEmbeddingModel(embeddingModelPath, isbinaryModel):
    word_vectors_model_size = os.path.getsize(embeddingModelPath) / (1024.0 * 1024.0)
    print("File size is {0:.2f}MB".format(word_vectors_model_size))
    if (isbinaryModel == True):
        print("Attempting to load embedding model as binary-format...")
        word_vectors_model = KeyedVectors.load_word2vec_format(embeddingModelPath, binary=True)
    else:
        print("Attempting to load embedding model as vector-format...")
        word_vectors_model = KeyedVectors.load_word2vec_format(embeddingModelPath, binary=False)
    print("Loading Successful!")
    return word_vectors_model


def stemEmbeddingWords(words):
    words = [w.lower() for w in words]
    stemWords=[stemmer.stem(w) for w in words]
    return stemWords


if __name__ == "__main__":
    main()

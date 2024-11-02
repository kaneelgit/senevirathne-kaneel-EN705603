from modules.extraction import preprocessing
import os
from modules.extraction import embedding

def preprocess_corpus(corpus_directory, chunking_stratergy, fixed_length = None, overlap_size = 2):

    #initialize preprocessing module
    pp = preprocessing.DocumentProcessing()

    #get all the files from directory
    files = os.listdir(corpus_directory)
    file_dirs = [os.path.join(corpus_directory, f) for f in files]

    #initialize embedding model
    embedding_model_name = 'all-MiniLM-L6-v2'
    embedding_model = embedding.Embedding(embedding_model_name)
    
    if chunking_stratergy == 'sentence':

        for dir in file_dirs:
            chunks = pp.sentence_chunking(dir, overlap_size=overlap_size)
            for chunk in chunks:
                sentence_embedding = embedding_model.encode(chunk)
                print(sentence_embedding)
                
preprocess_corpus('storage/corpus', 'sentence')


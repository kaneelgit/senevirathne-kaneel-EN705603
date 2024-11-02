from modules.extraction import preprocessing
import os
from modules.extraction import embedding

def preprocess_corpus(corpus_directory, chunking_stratergy, fixed_length = None, overlap_size = 2, faiss_index = False):

    #initialize preprocessing module
    pp = preprocessing.DocumentProcessing()

    #get all the files from directory
    files = os.listdir(corpus_directory)
    file_dirs = [os.path.join(corpus_directory, f) for f in files]

    #initialize embedding model
    embedding_model_name = 'all-MiniLM-L6-v2'
    embedding_model = embedding.Embedding(embedding_model_name)
    
    for dir in file_dirs:
        if chunking_stratergy == 'sentence':
            chunks = pp.sentence_chunking(dir, overlap_size=overlap_size)
        elif chunking_stratergy == 'fixed-length':
            chunks = pp.fixed_length_chunking(dir, fixed_length)
        else:
            chunks = []

    #embeddings
    embeddings = []
    for chunk in chunks:
        emb = embedding_model.encode(chunk)
        if faiss_index:
            faiss_index.add_embeddings(emb, metadata = chunk)
        embeddings.append(emb)

    if faiss_index:
        faiss_index.save("storage/catalog/faiss.index", "storage/catalog/metadata.pkl")

    return chunks, embeddings




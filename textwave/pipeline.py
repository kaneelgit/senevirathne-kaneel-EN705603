from modules.extraction import preprocessing
import os
from modules.extraction import embedding
from modules.retrieval.indexing import FaissIndex
from modules.retrieval.search import FaissSearch
from modules.retrieval import indexing
from modules.generator import question_answering
from modules.retrieval.reranking import Reranker

class Pipeline:

    def __init__(self, embedding_model_name = 'all-MiniLM-L6-v2', faiss_path = "../storage/catalog/faiss.index",\
                 metadata_path = "../storage/catalog/metadata.pkl", metric='euclidean', generator_model = "mistral-large-latest", \
                    api_key_path = '../api_key.json', temperature = 0.2):

        #initialize preprocessing module
        self.pp = preprocessing.DocumentProcessing()
        
        #initialize embedding model
        self.embedding_model = embedding.Embedding(embedding_model_name)
        
        #initialize faiss index
        faiss_index = indexing.FaissIndex()
        faiss_index.load(faiss_path = faiss_path, metadata_path = metadata_path)
        self.faiss_index_bf = FaissSearch(faiss_index, metric=metric)

        #generator model
        self.generator_model = generator_model

        #get api key
        with open(api_key_path, 'r') as file:
            self.api_key = file.readline().strip()

        #initialize generator
        self.generator = question_answering.QA_Generator(api_key = self.api_key, temperature=temperature, generator_model=generator_model)

    def _encode(self, query):
        """
        Embeds the given query using the embedding model initialized by the class
        """
        query_embedding = self.embedding_model.encode([query])

        return query_embedding

    def search_neighbors(self, query_embedding, k = 10):
        """
        search k nearest neighbours 
        """
        distances_ivf, indices_ivf, metadata_ivf = self.faiss_index_bf.search(query_embedding, k=k)
        return distances_ivf, metadata_ivf
    
    def generate_answer(self, query, context, rerank = True, rerank_type = "hybrid"):

        #rerank if rerank is true
        if rerank:
            reranker = Reranker(type=rerank_type)
            ranked_documents, ranked_indices, scores = reranker.rerank(query, context=context)
            context = ranked_documents

        #generate answer
        answer = self.generator.generate_answer(query, context)

        return query, answer, context
        
    def preprocess_corpus(self, corpus_directory, chunking_stratergy, fixed_length = None, overlap_size = 2, faiss_index = False, index_dir = None, metadata_dir = None):

        #get all the files from directory
        files = os.listdir(corpus_directory)
        file_dirs = [os.path.join(corpus_directory, f) for f in files]
        
        for dir in file_dirs:
            if chunking_stratergy == 'sentence':
                chunks = self.pp.sentence_chunking(dir, overlap_size=overlap_size)
            elif chunking_stratergy == 'fixed-length':
                chunks = self.pp.fixed_length_chunking(dir, fixed_length)
            else:
                chunks = []
        
        #embedding encode embeddings
        embeddings = self.embedding_model.encode(chunks)

        #if faiss index is given add data and save them
        if faiss_index:
            faiss_index.add_embeddings(embeddings, metadata = chunks)
            
            #get dir to save faiss index.
            index_dir = index_dir if index_dir else "storage/catalog/faiss.index"
            metadata_dir = metadata_dir if metadata_dir else "storage/catalog/metadata.pkl"   
            faiss_index.save(index_dir, metadata_dir)

        return chunks, embeddings



# def preprocess_corpus(corpus_directory, chunking_stratergy, fixed_length = None, overlap_size = 2, faiss_index = False, index_dir = None, metadata_dir = None):

#     #initialize preprocessing module
#     pp = preprocessing.DocumentProcessing()

#     #get all the files from directory
#     files = os.listdir(corpus_directory)
#     file_dirs = [os.path.join(corpus_directory, f) for f in files]

#     #initialize embedding model
#     embedding_model_name = 'all-MiniLM-L6-v2'
#     embedding_model = embedding.Embedding(embedding_model_name)
    
#     for dir in file_dirs:
#         if chunking_stratergy == 'sentence':
#             chunks = pp.sentence_chunking(dir, overlap_size=overlap_size)
#         elif chunking_stratergy == 'fixed-length':
#             chunks = pp.fixed_length_chunking(dir, fixed_length)
#         else:
#             chunks = []
    
#     #embedding encode embeddings
#     embeddings = embedding_model.encode(chunks)

#     #if faiss index is given add data and save them
#     if faiss_index:
#         faiss_index.add_embeddings(embeddings, metadata = chunks)
        
#         #get dir to save faiss index.
#         index_dir = index_dir if index_dir else "storage/catalog/faiss.index"
#         metadata_dir = metadata_dir if metadata_dir else "storage/catalog/metadata.pkl"   
#         faiss_index.save(index_dir, metadata_dir)

#     return chunks, embeddings

# faiss_index_bf = FaissIndex(index_type='brute_force', nlist=50)
# preprocess_corpus('storage/corpus_test', 'fixed-length', fixed_length = 50, overlap_size = 3, faiss_index = faiss_index_bf)

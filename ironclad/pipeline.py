from extraction import embedding, processing
import os
import numpy as np
from retrieval.index import FaissIndex
from retrieval.search import FaissSearch

class Pipeline:

    def __init__(self, image_size=160, model_device='cuda', faiss_index_type='Flat', gallery_dir='storage/gallery', catalog_dir='storage/catalog'):
        
        # Initialize the preprocessing and embedding components
        self.preprocessing = processing.Preprocessing(image_size=image_size)
        self.embedding_model = embedding.Embedding(device=model_device)
        self.faiss_index = FaissIndex(index_type=faiss_index_type)
        self.gallery_dir = gallery_dir
        self.catalog_dir = catalog_dir
        
    def _encode(self, image):
        # Preprocess the image
        preprocessed_image = self.preprocessing.process(image)
        # Compute the embedding
        embedding = self.embedding_model.encode(preprocessed_image)
        return embedding

    def _precompute(self, gallery_directory=None):
        """
        Precompute and store embeddings from all images in the gallery directory in a FAISS database.
        """
        gallery_directory = gallery_directory if gallery_directory else self.gallery_dir
        for root, dirs, files in os.walk(gallery_directory):
            for file in files:
                if file.endswith(('.png', '.jpg', '.jpeg')):
                    try:
                        # Load image
                        image_path = os.path.join(root, file)
                        image = Image.open(image_path)
                        
                        # Compute embedding
                        embedding = self._encode(image)
                    
                        # Add the embedding and associated metadata (file path and person name) to the FAISS index
                        person_name = os.path.basename(root)  # Assuming the directory name is the person's name
                        metadata = {"name": person_name, "image_filename": file}
                        
                        # Add embedding to FAISS index
                        embedding = np.expand_dims(embedding, axis=0)  # Add batch dimension to the embedding
                        self.faiss_index.add_embeddings(embedding, metadata=metadata)
                    except:
                        pass

    def _save_embeddings(self, faiss_path=None, metadata_path=None):
        """
        Save the FAISS index and associated metadata to disk in serialized format.
        """
        faiss_path = faiss_path if faiss_path else os.path.join(self.catalog_dir, "faiss.index")
        metadata_path = metadata_path if metadata_path else os.path.join(self.catalog_dir, "metadata.pkl")
        
        self.faiss_index.save(faiss_path, metadata_path)

    def search_gallery(self, probe, k=5):
        """
        Search for the k-nearest neighbors of a probe in the gallery and return their metadata.
        """
        # Encode the probe image
        embedding = self._encode(probe)
        embedding = np.expand_dims(embedding, axis=0)  # Add batch dimension
        
        # Perform a search in the FAISS index
        searcher = FaissSearch(self.faiss_index)
        distances, indices, metadata_results = searcher.search(embedding, k=k)
        
        # Compile the results with name, filename, and embedding vectors
        search_results = []
        for i, metadata in enumerate(metadata_results):
            result = {
                "name": metadata["name"],
                "image_filename": metadata["image_filename"],
                "embedding": self.faiss_index.index.reconstruct(int(indices[0][i]))
            }
            search_results.append(result)
        
        return search_results

from PIL import Image

image_path = "storage/probe/Alan_Ball/Alan_Ball_0002.jpg"
probe_image = Image.open(image_path)

pline = Pipeline(image_size=160, model_device='cuda')
pline._precompute()
pline._save_embeddings()
import pdb; pdb.set_trace()
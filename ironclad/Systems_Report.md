# System Report of IronClad visual search system

## System Design

### Overview ###

Ironclad is an advanced visual search system designed for efficient and accurate identity recognition. Leveraging Docker for scalable deployment, it processes images to extract unique embeddings, stores these embeddings in a structured format, and retrieves them based on user queries. Ironclad uses the pre-trained VGGFace2 model to create embeddings, which capture facial features for identity matching. For retrieval, it employs a Minkowski distance metric and performs a nearest neighbor search, allowing flexible search strategies with different FAISS indexing options to optimize speed and performance. These options include brute force, IVF (Inverted File Index), Flat, IVFPQ (Inverted File with Product Quantization), PQ (Product Quantization), and HNSW (Hierarchical Navigable Small World) indexes. The system also facilitates a method to add new identities to already existing FAISS Indexes which allows the system to be effectively used in a real world environment. 

![Diagram](diagrams.jpg)

### Preprocessing ###

The Preprocessing service standardizes incoming images by scaling, resizing, and normalizing them, creating a uniform set of inputs. This step is crucial because it removes inconsistencies in resolution, size, and color, ensuring that the VGGFace2 model can extract embeddings accurately. By preparing each image in a consistent format, the preprocessing stage enhances the reliability of the downstream embedding generation and retrieval process, providing a solid foundation for accurate facial feature extraction.

### Embedding ###

The Embedding service uses the pre-trained VGGFace2 model to convert each preprocessed image into a high-dimensional embedding, a vector representation that captures the unique features of the face. This embedding acts as a distinctive "fingerprint" for each image, enabling precise comparisons across images. By using VGGFace2, Ironclad leverages state-of-the-art facial recognition capabilities, producing embeddings that are robust and suitable for large-scale retrieval. These embeddings are essential for the system's ability to perform fast and accurate identity matching in the retrieval stage.

### Storage ###

The Storage service manages both the Catalog and Gallery components. The Catalog contains the FAISS index, which is a highly optimized data structure for storing and retrieving embeddings efficiently, as well as metadata about each indexed image. The FAISS index can be configured with various types, such as brute force, IVF, Flat, IVFPQ, PQ, and HNSW, to support different retrieval speeds and memory optimizations. This flexibility allows Ironclad to test and deploy the most efficient indexing method based on its application requirements. Meanwhile, the Gallery component stores the original images, serving as a reference after the retrieval process to display matched identities and also serving as a database to re-create indexes if neccessary.

### Retrieval Service ###

The Retrieval Service performs the core search function of Ironclad, using the FAISS index to find the k (a user requested value) nearest neighbors of a given embedding. By employing the Minkowski distance metric, it compares embeddings in the high-dimensional space to identify similar faces quickly and accurately. The Retrieval Service leverages the flexibility of the FAISS library, allowing for a range of index types (e.g., IVF, IVFPQ, HNSW) to optimize for speed and memory efficiency based on system demands. This service enables Ironclad to provide real-time or near-real-time identity matches, returning the most similar identities based on the Minkowski distance, making it ideal for applications that require rapid and reliable identity recognition.
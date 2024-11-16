# System Report of Textwave 

## System Design

### Overview ###

The TextWave system is composed of several integrated components designed to provide retrieval-augmented generation for query answering. Trained on a corpus containing relevant company information, the system can retrieve content from an already trained FAISS index in response to a query. The system includes an extraction module that generates the query embedding, a retrieval module that searches for relevant content in the index, a generator module that leverages the MISTRAL AI API to generate answers based on the retrieved content, and an interface module that uses Docker to facilitate communication with the user.

### Extraction Module ###

The extraction module consists of two key services: the preprocessing service and the embedding service. The preprocessing service handles document parsing using various chunking strategies to prepare the data for embedding. Once parsed, the processed documents are passed to the embedding service, which is responsible for generating embeddings using a specified model (e.g., 'all-MiniLM-L6-v2') and saving them in the FAISS index.

### Retrieval Module ###

The retrieval module consists of three key methods: the indexing method, the reranking method, and the search method. The indexing method is used to store the extracted embeddings from documents provided by company managers, which include company-related data. It supports various indexing strategies, offering flexibility in how the embeddings are stored. The search method retrieves the k nearest neighbors based on a query embedding. These k neighbors are then passed to the reranking method, which reorders the embeddings using different reranking techniques, such as hybrid, cross-encoder, TF-IDF, and others. 

### Generator Module ###

The generator module utilizes the MISTRAL AI API to generate answers to queries by combining the query with the k nearest neighbors (context) retrieved from the FAISS index created from the company’s corpus. The module allows the user to select a generator model from the available MISTRAL AI models, such as 'mistral-large-latest'.

### Interface Module ###

The interface module is a containerized application that provides two endpoints for interacting with the service. The /query endpoint allows users to input a question, which the system then preprocesses. It searches the index for relevant content, requests an answer from the MISTRAL API, and returns the generated response to the user. Users can adjust the number of k nearest neighbors, offering flexibility in the content passed to the API. The interface also has an endpoint /update_corpus to add new documents to the company corpus so that the index can be updated with new information. 

## Metrics Definition

### Offline Metrics ###

To evaluate the performance of the TextWave system, we use several offline metrics to ensure it 
retrieves accurate and relevant information for generating answers. One key metric is **exact match**, 
which checks if the content retrieved from the FAISS index perfectly matches the correct information 
in our test data. Another metric is **transformer matching**, which measures how similar the retrieved 
content is to the correct answers by comparing their meanings using a transformer model. This helps us 
understand whether the system is retrieving semantically relevant information, even if the words do not 
match exactly. Additionally, **manual feedback checking** is a critical metric: the system saves queries 
and answers, and expert human reviewers grade the results based on their accuracy and quality. 
This provides deeper insights into how well the system performs in real-world scenarios and helps 
identify areas for improvement. Together, these metrics ensure that the system consistently retrieves 
and generates high-quality responses.

### Online Metrics ###

To monitor and improve the real-time performance of the TextWave system, we use several online metrics that evaluate its responsiveness and 
user satisfaction. One key metric is response time, which measures the time taken to process a query and generate an answer. A fast response 
time is essential to ensure a smooth user experience. Another important metric is retrieval efficiency, which tracks how quickly the system 
searches the FAISS index and fetches the most relevant results, helping us assess the performance of the retrieval module under different query 
loads.

We also monitor generation latency, which measures the time taken by the generator module to produce an answer using the MISTRAL API. 
This helps us identify potential bottlenecks in the answer generation step. Additionally, user interaction metrics such as click-through 
rates (whether users act on the provided answers) and query abandonment rates (whether users leave without waiting for a response) provide 
insights into how well the system meets user expectations in real-time scenarios. Combining these metrics helps ensure the system remains 
efficient, accurate, and user-friendly during actual usage.

## System Parameters and Configurations



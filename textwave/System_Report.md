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

### Online Metrics ###

## System Parameters and Configurations


# Rag-Tag Project

## Introduction

This project explores a simple way to enhance RAG result qualty by applying symantic tags to each document.

A list of tags is generated for each document based on the subjects and topics it contains. A query is then matched not against the doc text, but against the symantic tags, and relevant documents are then retrieved and fused into a single list based on a cumulative score of their tag relevance.

Because tags are a mush shorter series of tokens, their similarity scores are much more relevant to the query than what you would get from larger blocks of text.

This approach has analogs, such as knowledge graphs, where relationships between document nodes are tracked using metadata.

Rag-Tag attempts to reduce the architecture overhead and complexity of a knowledge graph by utilizing the symantic information created by embeddings from granular subject tags.


## Purpose

The Rag-Tag project provides an architecture framework that can be integrated into your existing RAG platform to improve document lookup relevancy. This approach can be applied to chat history to retrieve relevant messages, or stored documents to provide relevant context.

We provide a data model via SQL files, a database abstraction layer, and a python library for performing RAG lookup.

We also provide a user interface for testing the RAG-TAG architecture.

## Technology Stack

- **OpenAI**: Used for embeddings as part of the lite install.

- **SQLite**: Used for relational storage, SQLite offers a lightweight, disk-based database that doesn't require a separate server process. It's ideal for storing the project's data model and efficiently handling relational data operations.

- **FAISS (Facebook AI Similarity Search)**: A library for efficient similarity search and clustering of dense vectors. FAISS is utilized for the vector store and vector similarity search (VSS), enabling fast and accurate retrieval of documents based on semantic similarity.

- **RAG Implementation as a Python Library**: The Retrieval-Augmented Generation (RAG) model is implemented as a Python library, facilitating the integration of retrieval-based mechanisms into generative models for enhanced document lookup and relevancy.

- (TODO) **Llama-index**: An abstraction layer for the vector store that integrates with the llmama ecosystem and provides features like RAG evals.

- (TODO) **Single-Page Application (SPA)**: An SPA is developed to test the RAG functionality, providing a user-friendly interface for interacting with the RAG system and evaluating its performance in real-time.

- (TODO) **FastAPI Server**: A FastAPI server is used for testing the RAG with the UI. FastAPI offers a high-performance, easy-to-use framework for building APIs, making it suitable for interfacing with the SPA and handling backend logic.

- (TODO) **Docker**: Both the database (SQLite) and the FastAPI server are designed to be Docker-based applications, ensuring easy deployment and scalability.

## Getting Started / Installation

To get started with the Rag-Tag project, follow these steps:

1. Clone the repository: 

    `git clone git@github.com:alekst23/rag-tag.git`
2. Start a virtual environment: 

    `python -m venv .venv; source .venv/bin/activate`

3. Install the dependencies: 

    a. For the basic setup using OpenAI for embeddings: 
        
    `pip install -r req-light.txt`

    `echo "export OPENAI_API_KEY=<your api key>" > .env`

    b. For llama based setup: 
    
    `pip install -r req-llama.txt`

4. Set up your database by running the SQL scripts provided in the `src/db/schema` directory.

5. (TODO) Start the FastAPI server: `python app.py`

6. (TODO) Open the Single-Page Application (SPA) in your browser and start testing the RAG functionality.


## Testing

### Running pytests

Run all tests

`make test`

### Notebook example

You can test RAG-TAG using [`run.ipynb`](run.ipynb)

## License

This project is licensed under the Apache License 2.0. For more information, please see the [LICENSE](LICENSE) file.

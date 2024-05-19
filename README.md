# Rag-Tag Project

## Introduction

The Rag-Tag project aims to explore a novel RAG architecture that utilizes a tag-document relationship and a rank fusion mechanism to create a better semantic relationship between multiple documents.

## Purpose

The Rag-Tag project provides an architecture framework that can be integrated into your RAG platform to improve document lookup relevancy. This approach can be applied to chat history to retrieve relevant messages, or stored documents to provide relevant context.

We provide a data model via SQL files, a database abstraction layer, and a python library for performing RAG lookup.

We also provide a user interface for testing the RAG-TAG architecture.

## Technology Stack

- **SQLite**: Used for relational storage, SQLite offers a lightweight, disk-based database that doesn't require a separate server process. It's ideal for storing the project's data model and efficiently handling relational data operations.

- **FAISS (Facebook AI Similarity Search)**: A library for efficient similarity search and clustering of dense vectors. FAISS is utilized for the vector store and vector similarity search (VSS), enabling fast and accurate retrieval of documents based on semantic similarity.

- **RAG Implementation as a Python Library**: The Retrieval-Augmented Generation (RAG) model is implemented as a Python library, facilitating the integration of retrieval-based mechanisms into generative models for enhanced document lookup and relevancy.

- **Single-Page Application (SPA)**: An SPA is developed to test the RAG functionality, providing a user-friendly interface for interacting with the RAG system and evaluating its performance in real-time.

- **FastAPI Server**: A FastAPI server is used for testing the RAG with the UI. FastAPI offers a high-performance, easy-to-use framework for building APIs, making it suitable for interfacing with the SPA and handling backend logic.

Both the database (SQLite) and the FastAPI server are designed to be Docker-based applications, ensuring easy deployment and scalability.

## Getting Started / Installation

To get started with the Rag-Tag project, follow these steps:

1. Clone the repository: `git clone https://github.com/your-username/rag-tag.git`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Set up the database by running the SQL scripts provided in the `database` directory.
4. Start the FastAPI server: `python app.py`
5. Open the Single-Page Application (SPA) in your browser and start testing the RAG functionality.

## Contribution Guidelines

If you would like to contribute to the Rag-Tag project, please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bug fix: `git checkout -b feature/your-feature-name` or `git checkout -b bugfix/your-bug-fix-name`
3. Make your changes and commit them: `git commit -m "Your commit message"`
4. Push your changes to your forked repository: `git push origin feature/your-feature-name` or `git push origin bugfix/your-bug-fix-name`
5. Open a pull request on the main repository and provide a detailed description of your changes.

We appreciate your contributions!

## License

This project is licensed under the Apache License 2.0. For more information, please see the [LICENSE](LICENSE) file.

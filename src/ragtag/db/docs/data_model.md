# Data Model Documentation

## Docs Table

The `docs` table is designed to store documents that can be tagged and retrieved through the system. Each document is stored with the following fields:

- `id`: A unique identifier for each document. It is an auto-incrementing integer.
- `text`: The content of the document. This field is capable of storing up to 32,768 characters, accommodating the maximum input length for the embedding model.

This table is essential for storing the raw text of documents that will be processed and tagged within the system.

## Tags Table

The `tags` table is designed to store unique tags associated with documents, along with their vector embeddings for similarity searches. The table includes:

- `tag`: A unique identifier for each tag, stored in a case-insensitive manner to ensure "Python" and "python" are treated equivalently.
- `embedding`: A binary field storing the vector embedding of the tag, used in vector similarity search operations.

This design supports efficient tag storage and retrieval, as well as advanced search capabilities through vector embeddings.

## Doc-Tags Join Table

The `doc_tags` join table is designed to establish a many-to-many relationship between the `docs` and `tags` tables. It includes:

- `doc_id`: Linked to the `docs` table, representing the document.
- `tag`: Linked to the `tags` table, representing the tag associated with the document.

This table supports efficient querying for documents based on tags and vice versa, facilitating advanced search and retrieval operations.

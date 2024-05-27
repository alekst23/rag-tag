# DocTagsDAO Method Documentation

This document provides detailed documentation for each method defined in the `DocTagsDAO` class, including expected inputs, outputs, and any side effects.

## Method Signatures and Behaviors

### 1. `add_tags_to_doc(doc_id: int, tag_ids: List[int]) -> None`
- **Description**: Adds a list of tag IDs to a specific document.
- **Parameters**:
  - `doc_id`: The ID of the document to which tags will be added.
  - `tag_ids`: A list of tag IDs to add to the document.
- **Outputs**: None.
- **Side Effects**: Inserts multiple entries into the `doc_tags` table, each linking the document with one of the specified tags.

### 2. `get_doc_tags(doc_id: int) -> List[str]`
- **Description**: Retrieves tags associated with a specific document.
- **Parameters**:
  - `doc_id`: The ID of the document for which to retrieve tags.
- **Outputs**: A list of tags associated with the document.
- **Side Effects**: None.

### 3. `get_tag_docs(tag: str) -> List[int]`
- **Description**: Retrieves documents associated with a specific tag.
- **Parameters**:
  - `tag`: The tag for which to retrieve associated documents.
- **Outputs**: A list of document IDs associated with the tag.
- **Side Effects**: None.

### 4. `remove_doc_tags(doc_id: int) -> None`
- **Description**: Removes all tags associated with a specific document.
- **Parameters**:
  - `doc_id`: The ID of the document from which to remove all tags.
- **Outputs**: None.
- **Side Effects**: Deletes all entries in the `doc_tags` table that link the specified document with any tag.

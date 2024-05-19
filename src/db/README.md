# Database Module

## Overview

This module contains utilities and classes for managing database connections and operations within the project. It's designed to centralize the logic for connecting to the SQLite database, ensuring efficient and consistent database access across the backend.

## Database Connection Utility

The `db_connection.py` file provides a utility class for managing SQLite database connections. This utility handles the creation and management of database connections, optionally incorporating connection pooling for improved performance.

### Usage

To use the database connection utility, import the `DBConnection` class from `db_connection.py` and create a new instance with the path to your SQLite database file. Then, use the `create_connection` method to establish a connection.

Example:

```python
from db_connection import DBConnection

database_path = "./path/to/database.sqlite"
db_connection = DBConnection(database_path)
conn = db_connection.create_connection()

if conn:
    # Perform database operations
    conn.close()
```

## Connection Pooling (Optional)

Connection pooling can be implemented to enhance performance by reusing existing database connections instead of creating new ones for each operation. This feature is optional and can be configured based on the project's requirements.

For more information on implementing connection pooling, refer to the documentation of the library or framework used for this purpose.

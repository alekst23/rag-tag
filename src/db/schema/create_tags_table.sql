-- Updated create_tags_table.sql

-- Drop the table if it already exists
DROP TABLE IF EXISTS tags;

-- Create the tags table
CREATE TABLE IF NOT EXISTS tags (
    tag TEXT PRIMARY KEY COLLATE NOCASE,
    embedding BLOB NOT NULL
);

-- Add any necessary changes or additions here

--

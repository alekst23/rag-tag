CREATE TABLE IF NOT EXISTS doc_tags (
    doc_id INTEGER,
    tag TEXT,
    PRIMARY KEY (doc_id, tag),
    FOREIGN KEY (doc_id) REFERENCES docs(id),
    FOREIGN KEY (tag) REFERENCES tags(tag)
);

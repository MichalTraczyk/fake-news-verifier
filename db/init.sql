CREATE EXTENSION IF NOT EXISTS vector;

-- where the knowledge came from
CREATE TABLE IF NOT EXISTS sources (
    id           BIGSERIAL PRIMARY KEY,
    url          TEXT UNIQUE,
    published_at TIMESTAMPTZ,  -- when the source was published (NULL if unknown)
    reliability  REAL NOT NULL DEFAULT 0.5 CHECK (reliability BETWEEN 0 AND 1),
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- part of knowledge e.g "Donald Truml married"
CREATE TABLE IF NOT EXISTS chunks (
    id           BIGSERIAL PRIMARY KEY,
    source_id    BIGINT REFERENCES sources(id) ON DELETE CASCADE, --one source can have many chunks
    content      TEXT NOT NULL,
    content_hash TEXT GENERATED ALWAYS AS (md5(content)) STORED,
    embedding    vector(1536) NOT NULL,
    metadata     JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (source_id, content_hash)
);

-- claims, eg. "Donald Trump is gay"
CREATE TABLE IF NOT EXISTS claims (
    id          BIGSERIAL PRIMARY KEY,
    claim       TEXT NOT NULL,
    embedding   vector(1536) NOT NULL,
    verdict     TEXT NOT NULL DEFAULT 'unverified'
                CHECK (verdict IN ('true', 'false', 'misleading', 'unverified')),
    confidence  REAL CHECK (confidence BETWEEN 0 AND 1),
    explanation TEXT,
    checked_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ties claims to chunks
CREATE TABLE IF NOT EXISTS claim_evidence (
    claim_id BIGINT REFERENCES claims(id) ON DELETE CASCADE,
    chunk_id BIGINT REFERENCES chunks(id) ON DELETE CASCADE,
    stance   TEXT NOT NULL CHECK (stance IN ('supports', 'refutes', 'neutral')),
    PRIMARY KEY (claim_id, chunk_id)
);

CREATE INDEX IF NOT EXISTS chunks_embedding_idx
    ON chunks USING hnsw (embedding vector_cosine_ops);
CREATE INDEX IF NOT EXISTS claims_embedding_idx
    ON claims USING hnsw (embedding vector_cosine_ops);
CREATE INDEX IF NOT EXISTS chunks_metadata_idx
    ON chunks USING gin (metadata);

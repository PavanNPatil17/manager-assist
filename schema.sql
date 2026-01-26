-- Create schema
CREATE SCHEMA IF NOT EXISTS cortex;

-- Set search path to use the schema
SET search_path TO cortex, public;

-- Create tables inside cortex schema
CREATE TABLE cortex.manager_memory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    org_id TEXT NOT NULL,
    user_id TEXT NOT NULL,

    -- Classification
    category TEXT[] NOT NULL,  -- Array of categories
    subcategory TEXT,

    title TEXT NOT NULL,
    summary TEXT NOT NULL,

    -- Structured meaning
    facts JSONB DEFAULT '{}',
    entities JSONB DEFAULT '{}',

    -- Lifecycle
    memory_date DATE,
    reminder_at TIMESTAMP NULL,
    confidence REAL CHECK (confidence >= 0 AND confidence <= 1),

    source TEXT NOT NULL,          -- manager_chat, email, web, etc.
    source_ref TEXT NULL,          -- email_id, url, etc.

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE INDEX idx_manager_memory_category ON cortex.manager_memory(category);
CREATE INDEX idx_manager_memory_date ON cortex.manager_memory(memory_date);
CREATE INDEX idx_manager_memory_facts ON cortex.manager_memory USING GIN (facts);
CREATE INDEX idx_manager_memory_entities ON cortex.manager_memory USING GIN (entities);
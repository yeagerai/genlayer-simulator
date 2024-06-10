CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    from_address VARCHAR(255),
    to_address VARCHAR(255),
    input_data JSONB,
    data JSONB,
    consensus_data JSONB,
    nonce INT,
    value NUMERIC,
    type INT CHECK (type IN (0, 1, 2)),
    gasLimit BIGINT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    r INT,
    s INT,
    v INT
);

CREATE TABLE IF NOT EXISTS current_state (
    id VARCHAR(255) PRIMARY KEY,
    data JSONB NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS validators (
    id SERIAL PRIMARY KEY,
    address VARCHAR(255),
    stake NUMERIC NOT NULL,
    provider VARCHAR(255),
    model VARCHAR(255),
    config JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

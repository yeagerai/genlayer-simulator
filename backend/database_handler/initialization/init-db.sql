-- Initialize the database if it doesn't exist
DO $$
DECLARE
    db_name TEXT := 'genlayer_state';  -- Set your desired database name here
    db_exists BOOLEAN;
BEGIN
    -- Check if the database already exists
    SELECT INTO db_exists EXISTS (
        SELECT 1 FROM pg_database WHERE datname = db_name
    );

    -- Only create the database if it does not exist
    IF NOT db_exists THEN
        -- Execute the CREATE DATABASE statement dynamically
        EXECUTE 'CREATE DATABASE ' || quote_ident(db_name);
        RAISE NOTICE 'Database % created successfully.', db_name;
    ELSE
        RAISE NOTICE 'Database % already exists.', db_name;
    END IF;
END $$;

CREATE TYPE transaction_status AS ENUM (
    'PENDING',
    'CANCELED',
    'PROPOSING',
    'COMMITTING',
    'REVEALING',
    'ACCEPTED',
    'FINALIZED',
    'UNDETERMINED'
);

CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    status transaction_status DEFAULT 'PENDING',
    from_address VARCHAR(255),
    to_address VARCHAR(255),
    input_data JSONB,
    data JSONB,
    consensus_data JSONB,
    nonce INT,
    value NUMERIC,
    type INT CHECK (type IN (0, 1, 2)),
    gaslimit BIGINT,
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

CREATE TABLE IF NOT EXISTS transactions_audit (
    id SERIAL PRIMARY KEY,
    transaction_id INT,
    data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
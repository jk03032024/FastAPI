
-- new lines added here -----
CREATE ROLE xlr8reader;
CREATE ROLE xlr8writer;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- account schema permissions to reader
-- permissions on existing objects in schema

GRANT USAGE ON SCHEMA account TO xlr8reader;
GRANT SELECT ON ALL TABLES IN SCHEMA account TO xlr8reader;

-- permissions on future objects in schema
ALTER DEFAULT PRIVILEGES IN SCHEMA account GRANT SELECT ON TABLES TO xlr8reader;

-- account schema permissions to writer
-- permissions on existing objects in schema
GRANT USAGE ON SCHEMA account TO xlr8writer;
GRANT CREATE ON SCHEMA account TO xlr8writer;
GRANT INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA account TO xlr8writer;
GRANT SELECT ON ALL TABLES IN SCHEMA account TO xlr8writer;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA account TO xlr8writer;

-- permissions on future objects in schema
ALTER DEFAULT PRIVILEGES IN SCHEMA account GRANT INSERT, UPDATE, DELETE ON TABLES TO xlr8writer;
ALTER DEFAULT PRIVILEGES IN SCHEMA account GRANT SELECT ON TABLES TO xlr8writer;
ALTER DEFAULT PRIVILEGES IN SCHEMA account GRANT USAGE, SELECT ON SEQUENCES TO xlr8writer;
ALTER DEFAULT PRIVILEGES IN SCHEMA account GRANT EXECUTE ON FUNCTIONS TO xlr8writer;
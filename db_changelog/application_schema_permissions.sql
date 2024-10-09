
-- application schema permissions to reader
-- permissions on existing objects in schema
GRANT USAGE ON SCHEMA application TO xlr8reader;
GRANT SELECT ON ALL TABLES IN SCHEMA application TO xlr8reader;

-- permissions on future objects in schema
ALTER DEFAULT PRIVILEGES IN SCHEMA application GRANT SELECT ON TABLES TO xlr8reader;

-- application schema permissions to writer
-- permissions on existing objects in schema
GRANT USAGE ON SCHEMA application TO xlr8writer;
GRANT CREATE ON SCHEMA application TO xlr8writer;
GRANT INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA application TO xlr8writer;
GRANT SELECT ON ALL TABLES IN SCHEMA application TO xlr8writer;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA application TO xlr8writer;

-- permissions on future objects in schema
ALTER DEFAULT PRIVILEGES IN SCHEMA application GRANT INSERT, UPDATE, DELETE ON TABLES TO xlr8writer;
ALTER DEFAULT PRIVILEGES IN SCHEMA application GRANT SELECT ON TABLES TO xlr8writer;
ALTER DEFAULT PRIVILEGES IN SCHEMA application GRANT USAGE, SELECT ON SEQUENCES TO xlr8writer;
ALTER DEFAULT PRIVILEGES IN SCHEMA application GRANT EXECUTE ON FUNCTIONS TO xlr8writer;
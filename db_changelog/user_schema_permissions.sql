
-- users schema permissions to reader
-- permissions on existing objects in schema
GRANT USAGE ON SCHEMA users TO xlr8reader;
GRANT SELECT ON ALL TABLES IN SCHEMA users TO xlr8reader;

-- permissions on future objects in schema
ALTER DEFAULT PRIVILEGES IN SCHEMA users GRANT SELECT ON TABLES TO xlr8reader;

-- users schema permissions to writer
-- permissions on existing objects in schema
GRANT USAGE ON SCHEMA users TO xlr8writer;
GRANT CREATE ON SCHEMA users TO xlr8writer;
GRANT INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA users TO xlr8writer;
GRANT SELECT ON ALL TABLES IN SCHEMA users TO xlr8writer;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA users TO xlr8writer;

-- permissions on future objects in schema
ALTER DEFAULT PRIVILEGES IN SCHEMA users GRANT INSERT, UPDATE, DELETE ON TABLES TO xlr8writer;
ALTER DEFAULT PRIVILEGES IN SCHEMA users GRANT SELECT ON TABLES TO xlr8writer;
ALTER DEFAULT PRIVILEGES IN SCHEMA users GRANT USAGE, SELECT ON SEQUENCES TO xlr8writer;
ALTER DEFAULT PRIVILEGES IN SCHEMA users GRANT EXECUTE ON FUNCTIONS TO xlr8writer;
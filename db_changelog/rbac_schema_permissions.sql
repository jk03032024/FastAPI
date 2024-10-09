
-- rbac schema permissions to reader
-- permissions on existing objects in schema
GRANT USAGE ON SCHEMA rbac TO xlr8reader;
GRANT SELECT ON ALL TABLES IN SCHEMA rbac TO xlr8reader;

-- permissions on future objects in schema
ALTER DEFAULT PRIVILEGES IN SCHEMA rbac GRANT SELECT ON TABLES TO xlr8reader;

-- rbac schema permissions to writer
-- permissions on existing objects in schema
GRANT USAGE ON SCHEMA rbac TO xlr8writer;
GRANT CREATE ON SCHEMA rbac TO xlr8writer;
GRANT INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA rbac TO xlr8writer;
GRANT SELECT ON ALL TABLES IN SCHEMA rbac TO xlr8writer;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA rbac TO xlr8writer;

-- permissions on future objects in schema
ALTER DEFAULT PRIVILEGES IN SCHEMA rbac GRANT INSERT, UPDATE, DELETE ON TABLES TO xlr8writer;
ALTER DEFAULT PRIVILEGES IN SCHEMA rbac GRANT SELECT ON TABLES TO xlr8writer;
ALTER DEFAULT PRIVILEGES IN SCHEMA rbac GRANT USAGE, SELECT ON SEQUENCES TO xlr8writer;
ALTER DEFAULT PRIVILEGES IN SCHEMA rbac GRANT EXECUTE ON FUNCTIONS TO xlr8writer;
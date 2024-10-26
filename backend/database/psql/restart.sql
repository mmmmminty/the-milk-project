-- Drop all tables in the current database
DO $$ DECLARE
        r RECORD;
BEGIN
        -- Disable triggers to avoid foreign key constraints issues
        EXECUTE 'ALTER TABLE ALL IN SCHEMA public DISABLE TRIGGER ALL';
        
        -- Drop all tables
        FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
        END LOOP;
        
        -- Enable triggers back
        EXECUTE 'ALTER TABLE ALL IN SCHEMA public ENABLE TRIGGER ALL';
END $$;
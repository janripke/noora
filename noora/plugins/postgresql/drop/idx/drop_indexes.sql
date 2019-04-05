DO $$
  BEGIN
    EXECUTE (
        SELECT 'DROP INDEX ' || string_agg(indexname, ', ')
        FROM pg_indexes
        WHERE schemaname='public'
    );
  END
$$;
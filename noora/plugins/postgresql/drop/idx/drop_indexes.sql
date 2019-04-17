DO $$
  DECLARE
    sttmnt VARCHAR;
  BEGIN
    FOR sttmnt IN
      SELECT 'DROP INDEX ' || string_agg(indexname, ', ')
      FROM pg_indexes
      WHERE schemaname='public'
    LOOP
      EXECUTE sttmnt;
    END LOOP;
  END;
$$
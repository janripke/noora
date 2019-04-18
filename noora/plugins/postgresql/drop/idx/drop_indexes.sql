DO $$
  DECLARE
    sttmnt VARCHAR;
  BEGIN
    FOR sttmnt IN
      SELECT 'DROP INDEX ' || string_agg(indexname, ', ')
      FROM pg_indexes
      WHERE schemaname='public'
    LOOP
      IF sttmnt IS NOT NULL THEN
          EXECUTE sttmnt;
      END IF;
    END LOOP;
  END;
$$
DO $$
  DECLARE
    sttmnt VARCHAR;
  BEGIN
    FOR sttmnt IN
      SELECT 'DROP VIEW ' || schemaname || '.' || viewname
      FROM pg_views
      WHERE viewowner = '{username}'
    LOOP
      EXECUTE sttmnt;
    END LOOP;
  END;
$$
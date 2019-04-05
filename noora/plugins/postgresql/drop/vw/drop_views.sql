DO $$
  DECLARE
    sttmnt VARCHAR;
  BEGIN
    FOR sttmnt IN
      SELECT 'DROP VIEW ' || table_schema || '.' || table_name
      FROM information_schema.views
      WHERE table_catalog='acme' and table_schema='public'
    LOOP
      EXECUTE sttmnt;
    END LOOP;
  END;
$$
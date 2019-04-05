DO $$
  DECLARE
    sttmnt VARCHAR;
  BEGIN
    FOR sttmnt IN
      SELECT 'DROP TRIGGER ' || trigger_name || ' ON ' || event_object_table
      FROM information_schema.triggers
      WHERE trigger_catalog='acme' and trigger_schema='public'
    LOOP
      EXECUTE sttmnt;
    END LOOP;
  END;
$$
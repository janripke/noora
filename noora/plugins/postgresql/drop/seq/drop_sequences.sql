DO $$
  DECLARE
    sttmnt VARCHAR;
  BEGIN
    FOR sttmnt IN
      SELECT 'DROP SEQUENCE ' || sequence_schema || '.' || sequence_name
      FROM information_schema.sequences
      WHERE sequence_catalog='acme' and sequence_schema='public'
    LOOP
      EXECUTE sttmnt;
    END LOOP;
  END;
$$
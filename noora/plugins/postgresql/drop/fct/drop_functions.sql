DO $$
  DECLARE
    sttmnt VARCHAR;
  BEGIN
    FOR sttmnt IN
      SELECT 'DROP FUNCTION ' || n.nspname || '.' || proname
                 || '(' || oidvectortypes(proargtypes) || ');'
      FROM pg_proc LEFT JOIN pg_namespace n ON pronamespace=n.OID
      WHERE n.nspname = 'public'
    LOOP
      EXECUTE sttmnt;
    END LOOP;
  END
$$

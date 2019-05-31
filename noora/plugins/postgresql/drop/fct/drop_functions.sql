DO $$
  DECLARE
    sttmnt VARCHAR;
  BEGIN
    FOR sttmnt IN
      SELECT 'DROP FUNCTION ' || n.nspname || '.' || p.proname || '(' || oidvectortypes(proargtypes) || ');'
      FROM pg_proc p
      LEFT JOIN pg_namespace n ON p.pronamespace = n.oid
      LEFT JOIN pg_roles r ON p.proowner=r.oid
      WHERE n.nspname='public'
      AND r.rolname='{username}'
    LOOP
      EXECUTE sttmnt;
    END LOOP;
  END
$$
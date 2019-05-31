DO $$
  DECLARE
    sttmnt VARCHAR;
  BEGIN
    FOR sttmnt IN
      SELECT 'DROP TABLE ' || table_schema || '.' || table_name
      FROM   information_schema.tables
      WHERE  table_catalog = '{database}'
      AND    table_schema  = 'public'
      AND    table_type    = 'BASE TABLE'
    LOOP
      EXECUTE sttmnt;
    END LOOP;
  END;
$$


-- select * from information_schema.tables WHERE table_catalog='meta' and table_type='BASE TABLE' and table_schema='public'
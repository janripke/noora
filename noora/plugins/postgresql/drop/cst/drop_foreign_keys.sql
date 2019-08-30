DO $$
  DECLARE
    sttmnt VARCHAR;
  BEGIN
    FOR sttmnt IN
      SELECT 'ALTER TABLE ' || table_schema || '.' || table_name || ' drop constraint ' || constraint_name
      FROM   information_schema.table_constraints
      WHERE  constraint_catalog = '{database}'
      AND    constraint_schema  = 'public'
      AND   constraint_type    = 'FOREIGN KEY'
    LOOP
      EXECUTE sttmnt;
    END LOOP;
  END;
$$


-- select * from information_schema.tables WHERE table_catalog='meta' and table_type='BASE TABLE' and table_schema='public'
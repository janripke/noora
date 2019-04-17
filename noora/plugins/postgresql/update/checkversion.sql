DO $$
  DECLARE
    version VARCHAR;
  BEGIN
    SELECT value INTO STRICT version
    FROM application_properties
    WHERE name='application.version' AND VALUE='{previous}';
    EXCEPTION
      WHEN NO_DATA_FOUND THEN
        RAISE EXCEPTION 'Version mismatch: {previous} expected';
  END;
$$

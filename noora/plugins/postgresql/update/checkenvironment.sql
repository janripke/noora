DO $$
  DECLARE
    environment VARCHAR;
  BEGIN
    SELECT value INTO STRICT environment
    FROM application_properties
    WHERE name='application.environment' AND VALUE='{environment}';
    EXCEPTION
      WHEN NO_DATA_FOUND THEN
      RAISE EXCEPTION 'Environment mismatch: {environment} expected';
  END;
$$
CREATE FUNCTION application_properties_bu() RETURNS trigger
AS $$
  BEGIN
    NEW.updated_at := CURRENT_TIMESTAMP;
    NEW.updated_by := CURRENT_USER;
    RETURN NEW;
  END
$$ LANGUAGE plpgsql;

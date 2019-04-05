CREATE FUNCTION application_properties_bi() RETURNS trigger
AS $$
  BEGIN
	NEW.created_at := current_timestamp;
    NEW.created_by := current_user;
    NEW.updated_at := NEW.created_at;
    NEW.updated_by := NEW.created_by;
    RETURN NEW;
  END;
$$ LANGUAGE plpgsql;

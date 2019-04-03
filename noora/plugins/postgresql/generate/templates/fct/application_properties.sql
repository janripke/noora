CREATE FUNCTION get_property (p_name VARCHAR) RETURNS VARCHAR
AS $$
  SELECT "value" FROM application_properties WHERE name=p_name;
$$ LANGUAGE SQL;


CREATE FUNCTION application_properties_bu_fct() RETURNS trigger
AS $$
  BEGIN
    NEW.updated_at := CURRENT_TIMESTAMP;
    NEW.updated_by := CURRENT_USER;
    RETURN NEW;
  END
$$ LANGUAGE plpgsql;


CREATE FUNCTION application_properties_bi_fct() RETURNS trigger
AS $$
  BEGIN
	NEW.created_at := current_timestamp;
    NEW.created_by := current_user;
    NEW.updated_at := NEW.created_at;
    NEW.updated_by := NEW.created_by;
  END;
$$

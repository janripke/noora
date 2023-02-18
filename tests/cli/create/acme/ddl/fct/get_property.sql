CREATE FUNCTION get_property (p_name VARCHAR) RETURNS VARCHAR
AS $$
  SELECT "value" FROM application_properties WHERE name=p_name;
$$ LANGUAGE SQL;

CREATE TRIGGER application_properties_bu
  BEFORE UPDATE ON application_properties
  EXECUTE PROCEDURE application_properties_bu_fct

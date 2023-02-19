CREATE TRIGGER application_properties_bu
  BEFORE UPDATE ON application_properties
  FOR EACH ROW
  EXECUTE PROCEDURE application_properties_bu();
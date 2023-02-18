CREATE TRIGGER application_properties_bi
  BEFORE INSERT ON application_properties
  FOR EACH ROW
  EXECUTE PROCEDURE application_properties_bi();
delimiter |

CREATE TRIGGER application_properties_bi BEFORE INSERT ON application_properties
  FOR EACH ROW BEGIN
	SET NEW.created_at=NOW();
    SET NEW.created_by=CURRENT_USER();
    SET NEW.updated_at=NOW();
    SET NEW.updated_by=CURRENT_USER();
  END;
|

delimiter ;
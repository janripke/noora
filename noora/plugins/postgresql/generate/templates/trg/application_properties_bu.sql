delimiter |

CREATE TRIGGER application_properties_bu
  BEFORE UPDATE ON application_properties
    FOR EACH ROW BEGIN
      SET NEW.updated_at=NOW();
      SET NEW.updated_by=CURRENT_USER();
    END;
|

delimiter ;


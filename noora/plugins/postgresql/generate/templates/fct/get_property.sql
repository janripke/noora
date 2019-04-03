delimiter |

CREATE FUNCTION get_property (p_name VARCHAR(255)) RETURNS VARCHAR(255)
  AS
    SELECT value INTO l_result FROM application_properties WHERE name=p_name;
  RETURN l_result;
END;
|
delimiter ;

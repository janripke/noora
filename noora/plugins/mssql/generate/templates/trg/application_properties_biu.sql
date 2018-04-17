CREATE or alter TRIGGER application_properties_biu ON application_properties AFTER INSERT, UPDATE
  AS
  BEGIN

  	-- insert operation
    IF NOT EXISTS (SELECT * FROM deleted)
	BEGIN
		UPDATE application_properties
		 SET created_at = GETDATE(),
			 created_by = CURRENT_USER,
			 updated_at = GETDATE(),
			 updated_by = CURRENT_USER
		FROM inserted
		WHERE application_properties.id = inserted.id;
	END

	-- update operation
	IF EXISTS (SELECT * FROM deleted)
	BEGIN
		UPDATE application_properties
		 SET updated_at = GETDATE(),
			 updated_by = CURRENT_USER
		FROM inserted
		WHERE application_properties.id = inserted.id;
	END
  END
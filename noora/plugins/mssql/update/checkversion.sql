begin
declare @result varchar(4000)
    set @result = (select value
                   from   application_properties
                   where  name = 'application.version')
	if @result != '{previous}'
	begin
		declare @message varchar(255) = 'incorrect database version, current: ' + @result +
		                                ', expected: {previous}'
		RAISERROR (@message,  18, 20)
	end
end
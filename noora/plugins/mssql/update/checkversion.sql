begin
declare @result varchar(4000)
    set @result = (select value
                   from   application_properties
                   where  name = 'application.version'
				   and    value = '{previous}')
	if @result is null
	begin
		declare @message varchar(255) = 'incorrect database version, the found version is ' + '{previous}'
		RAISERROR (@message,  18, 20)
	end
end
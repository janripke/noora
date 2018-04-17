begin
declare @result varchar(4000)
    set @result = (select value
                   from   application_properties
                   where  name = 'application.environment'
				   and    value = '{environment}')
	if @result is null
	begin
		declare @message varchar(255) = 'incorrect database environment, expected ' + '{environment}'
		RAISERROR (@message,18,20)
	end
end
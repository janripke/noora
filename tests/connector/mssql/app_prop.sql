create function app_prop__get_property(@name varchar(255))
returns varchar(4000)
as
begin
    DECLARE @result varchar(4000)
    set @result = (select value
                   from   application_properties
                   where  name = @name)
    if @result is null
    begin
        RAISERROR(59998, 16, 1, 'The record does not exist.');
    end;
    return @result
end

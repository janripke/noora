create function apy_get_property(@name varchar(255), @default varchar(255) = '')
returns varchar(4000)
as
begin
    declare @result varchar(4000)
    set @result = (select value
                   from   application_properties
                   where  name = @name)
    if @result is null
    begin
        if @default is null
            return cast('Error. Can''t find property with name: ' + @name + '...' as varchar(4000))
        return @default
    end
    return @result
end
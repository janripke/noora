create function get_property(@name varchar(255))
returns varchar(4000)
as
begin
    return (select value
                   from   application_properties
                   where  name = @name)
end

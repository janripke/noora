create function get_env(@name varchar(20))
returns varchar(20)
as
begin
    return @name
end

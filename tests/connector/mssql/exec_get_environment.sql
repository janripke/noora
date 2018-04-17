begin
    declare @result varchar(4000);
    set @result = (select value from application_properties where name='env');
    if @result is null
    begin
        RAISERROR(59998, 16, 1, 'The record does not exist.');
    end;
end;
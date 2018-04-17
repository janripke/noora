declare @sql nvarchar(500)
declare @cursor cursor

set @cursor = cursor fast_forward for

select distinct sql = 'drop function ' + schema_name(t.schema_id) + '.' + t.name
from {database}.sys.objects t
where schema_name(t.schema_id) = '{schema}'
and   t.type = 'FN'

open @cursor fetch next from @cursor into @sql

while (@@fetch_status = 0)
begin
    --Exec sp_executesql @Sql
    print @Sql
    Exec sp_executesql @Sql
    fetch next from @cursor into @sql
end

close @cursor deallocate @cursor

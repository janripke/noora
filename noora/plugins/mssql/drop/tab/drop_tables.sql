declare @sql nvarchar(500)
declare @cursor cursor

set @cursor = cursor fast_forward for

select distinct sql = 'drop table ' + t.TABLE_CATALOG + '.' + t.TABLE_SCHEMA + '.' + t.TABLE_NAME
from information_schema.TABLES t
where t.TABLE_TYPE    = 'BASE TABLE'
and   t.table_catalog = '{database}'
and   t.table_schema  = '{schema}'

open @cursor fetch next from @cursor into @sql

while (@@fetch_status = 0)
begin
    Exec sp_executesql @Sql
    --print @sql
    fetch next from @cursor into @sql
end

close @cursor deallocate @cursor
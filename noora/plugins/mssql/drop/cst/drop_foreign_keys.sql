declare @sql nvarchar(4000)
declare @cursor CURSOR

set @cursor = cursor fast_forward for

select distinct sql = 'ALTER TABLE ' + t.table_catalog + '.' + t.table_schema + '.' + t.table_name + ' DROP [' + c.constraint_name + ']'
from information_schema.referential_constraints c
left join information_schema.table_constraints t on c.constraint_name =t.constraint_name
where   t.table_catalog = '{database}'
and     t.table_schema  = '{schema}'

open @cursor fetch next from @cursor into @sql

while (@@fetch_status = 0)
begin
    Exec sp_executesql @Sql
    print @sql
    fetch next from @cursor into @sql
end

close @cursor deallocate @cursor

-- declare @sql nvarchar(500)
-- declare @cursor cursor
--
-- set @cursor = cursor fast_forward for
--
-- select distinct sql = 'drop table ' + t.TABLE_CATALOG + '.' + t.TABLE_SCHEMA + '.' + t.TABLE_NAME
-- from information_schema.TABLES t
-- where t.TABLE_TYPE    = 'BASE TABLE'
-- and   t.table_catalog = '{database}'
-- and   t.table_schema  = '{schema}'
--
-- open @cursor fetch next from @cursor into @sql
--
-- while (@@fetch_status = 0)
-- begin
--     Exec sp_executesql @Sql
--     --print @sql
--     fetch next from @cursor into @sql
-- end
--
-- close @cursor deallocate @cursor
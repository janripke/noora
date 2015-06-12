set foreign_key_checks = 0;
select concat('drop table ',group_concat(table_name)) into @var_table_name from information_schema.tables where table_schema='{database}';
select @var_table_name;
select if(@var_table_name is NULL,'select "no tables" from dual',@var_table_name) into @var_table_name;
prepare stmt from @var_table_name;
execute stmt;
set foreign_key_checks = 1;
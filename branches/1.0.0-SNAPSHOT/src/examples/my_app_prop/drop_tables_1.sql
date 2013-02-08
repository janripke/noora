select concat('drop table ',group_concat(table_name)) into @var_table_name from information_schema.TABLES where table_schema='orcl';
select @var_table_name;
select if(@var_table_name is NULL,'select "no tables" from dual',@var_table_name) into @var_table_name;
prepare stmt from @var_table_name;
execute stmt;

#delimiter $$
#show tables;
#select count(*) into @var_table_count from information_schema.tables where table_schema='orcl';
select concat('drop table ',group_concat(table_name)) into @var_table_name from information_schema.TABLES where table_schema='orcl';
#select @var_table_count;
select @var_table_name;
#  select @var_table_name;
#  prepare stmt from @var_table_name;
#  execute stmt;
#  show tables;
i#delimiter ;

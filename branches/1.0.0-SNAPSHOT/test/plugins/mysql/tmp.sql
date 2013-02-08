select concat('drop function ',group_concat(specific_name)) into @var_specific_name from information_schema.routines where routine_schema='orcl' and routine_type='FUNCTION';
select @var_specific_name;
select if(@var_specific_name is NULL,'select "no functions" from dual',@var_specific_name) into @var_specific_name;
prepare stmt from @var_specific_name;
execute stmt;
delete 
  from mysql.proc 
 where name in 
   (select routine_name 
      from information_schema.routines 
     where routine_schema = '{database}'
       and routine_type   = 'FUNCTION'
     );
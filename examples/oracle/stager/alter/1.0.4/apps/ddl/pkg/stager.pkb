create or replace package body stager as

  M_QUOTE            constant varchar2(256):=chr(39);
  M_PACKAGE_NAME     constant varchar2(256):=lower($$plsql_unit);

  M_TAB              constant varchar2(1):=chr(9);


  function get_error_table
    (p_job_name   in varchar2
    ,p_table_name in varchar2) return varchar2 is

    l_result         varchar2(256);
    l_prc_name       varchar2(50):='get_error_table';
  begin

    select table_name
      into l_result
      from user_tab_comments
     where comments like 'DML Error Logging table for%'
       and replace(app_utl.get_column(comments,' ',6),'"','')=upper(p_table_name)
       and table_name not like 'BIN%';

    logger.debug(p_job_name, M_PACKAGE_NAME, l_prc_name, p_table_name || ' has ' || l_result || ' as error table');
    return l_result;
  exception
    when no_data_found then
      logger.error(p_job_name, M_PACKAGE_NAME, l_prc_name, 'error table not found for table ' || p_table_name);
      return null;
  end get_error_table;


  function stage
    (p_job_name          in varchar2
    ,p_file_id           in number
    ,p_table_name        in varchar2
    ,p_stage_table_name  in varchar2
    ,p_field_list        in app_utl.t_field_list) return number is

    pragma autonomous_transaction;

    l_statement  varchar2(32000);
    l_prc_name   varchar2(255):='stage';
    l_count      number(12):=0;
    l_fields     varchar2(4000);
    l_stage_error_table varchar2(30);

  begin
    l_fields:=app_utl.field_list_to_varchar
      (p_field_list => p_field_list
      ,p_delimiter  => ',');
      
    l_stage_error_table := get_error_table(p_job_name => p_job_name, p_table_name => p_stage_table_name);

    l_statement:='insert /*+ APPEND */ into ' || p_stage_table_name                ||
                 '('                                                 ||
                 'file_id '                                          ||
                 ',line_id '                                         ||
                 ',job_name '                                        ||
                 ',' || l_fields                                     ||
                 ')'                                                 ||
                 ' select ' || p_file_id                             ||
                          ',rownum'                                  ||
                          ',' || M_QUOTE ||  p_job_name || M_QUOTE   ||
                          ',' || l_fields                            ||
                 ' from   ' || p_table_name                          ||
                 ' log errors into ' || l_stage_error_table          ||
                 ' reject limit unlimited';

    logger.debug(p_job_name,M_PACKAGE_NAME,l_prc_name,substr(l_statement, 1, 4000));
    execute immediate l_statement;
    l_count:=SQL%ROWCOUNT;
    commit;
    logger.info(p_job_name,M_PACKAGE_NAME,l_prc_name,l_count || ' records(s) staged.');
    return l_count;

  end stage;
  
  function stage_bulk
    (p_job_name          in varchar2
    ,p_file_id           in number
    ,p_table_name        in varchar2
    ,p_stage_table_name  in varchar2
    ,p_field_list        in app_utl.t_field_list) return number is

    l_statement  varchar2(32000);
    l_prc_name   varchar2(255):='stage_bulk';
    l_count      number(12):=0;
    l_fields     varchar2(4000);
    l_stage_error_table varchar2(30);
    l_COMMIT_SIZE number := 5000;

  begin
      
    l_stage_error_table := stager.get_error_table(p_job_name => p_job_name, p_table_name => p_stage_table_name);
    l_fields:=app_utl.field_list_to_varchar
      (p_field_list => p_field_list
      ,p_delimiter  => ',');
  
    
    l_statement := 'declare 
  cursor c_ext is
    select rownum rownumr, ' || l_fields || ' from ' || p_table_name || ';
    type t_ext is table of c_ext%rowtype index by pls_integer;    
    r_ext t_ext;
    l_cnt number :=0;
  begin
  open c_ext;
  loop
      fetch c_ext bulk collect
        into r_ext limit ' ||  l_COMMIT_SIZE || ';
      forall i in r_ext.first .. r_ext.last
        insert into ' || p_stage_table_name || ' (file_id,line_id,job_name,' || l_fields || ') 
        values (' || p_file_id || ',r_ext(i).rownumr,''' || p_job_name || ''',r_ext(i).' || replace(l_fields, ',', ',r_ext(i).') || ')
        log errors into ' || l_stage_error_table || ' reject limit unlimited;
        l_cnt := l_cnt + sql%rowcount;
      commit;
    exit when c_ext%notfound;
  end loop;
  close c_ext;
  :recordcount := l_cnt;
end;'; 

    logger.debug(p_job_name,M_PACKAGE_NAME,l_prc_name,substr(l_statement, 1, 4000));
    execute immediate l_statement using out l_count;
    commit;
    logger.info(p_job_name,M_PACKAGE_NAME,l_prc_name,l_count || ' records(s) staged.');
    return l_count;
  end stage_bulk;

  procedure log_error_records
    (p_job_name in varchar2) is

    cursor     c_stage_error(b_job_name varchar2) is
      select   ora_err_mesg, count(1) nr_of_errors
      from     stage_error
      where    job_name = b_job_name
      group by ora_err_mesg
      order by ora_err_mesg;
    l_prc_name  varchar2(255):='log_error_records';
  begin
    for r_stage_error in c_stage_error(p_job_name)
    loop
      logger.error(p_job_name, M_PACKAGE_NAME, l_prc_name, replace(r_stage_error.ora_err_mesg, chr(10)) || ': ' || r_stage_error.nr_of_errors || ' errors');
    end loop;

  end log_error_records;

  procedure write_log_records
    (p_job_name in varchar2
    ,p_handle   in utl_file.file_type) is

    cursor c_log(b_job_name varchar2) is
      select id
            ,logtype_code
            ,job_name
            ,package_name
            ,method_name
            ,message
            ,created_at
            ,created_by
      from   log
      where  job_name=b_job_name;

    r_log     c_log%rowtype;
    l_line    varchar2(32000);

  begin
    for r_log in c_log(p_job_name)
    loop
      l_line:=to_char(r_log.created_at,'dd/mm/yyyy hh24:mi:ss')                          || M_TAB ||
              r_log.created_by                                                           || M_TAB ||
              r_log.logtype_code                                                         || M_TAB ||
              '[' || lower(r_log.package_name) || '.' || lower(r_log.method_name) || ']' || M_TAB ||
              r_log.message;

      utl_file.put_line(p_handle,l_line);

    end loop;
  end;



  procedure create_log_file
    (p_job_name    in varchar2
    ,p_folder      in varchar2
    ,p_filename    in varchar2) is


    l_handle                utl_file.file_type;
    l_prc_name              varchar2(255):='create_log_file';

  begin

    l_handle:=app_utl.open_file
      (p_folder    => p_folder
      ,p_filename  => p_filename
      ,p_open_mode => 'w');

    write_log_records
      (p_job_name => p_job_name
      ,p_handle   => l_handle);

    app_utl.close_file(l_handle,p_filename);
  end;



  procedure write_ni_header
    (p_job_name    in varchar2
    ,p_handle      in utl_file.file_type
    ,p_file_header in varchar2) is
  begin
     utl_file.put_line(p_handle,p_file_header);
  end;



  function get_stage_line
    (p_job_name          in varchar2
    ,p_table_name        in varchar2
    ,p_id                in number
    ,p_field_list        in app_utl.t_field_list
    ,p_delimiter         in varchar2) return varchar2 is

    l_statement  varchar2(32000);
    l_prc_name   varchar2(255):='stage';
    l_count      number(12):=0;
    l_fields     varchar2(4000);
    l_result     varchar2(4000);

  begin
    l_fields:=app_utl.field_list_to_varchar
      (p_field_list => p_field_list
      ,p_delimiter  => '|| ' || M_QUOTE || p_delimiter || M_QUOTE || ' ||');

    l_statement:=' begin ' ||
                 '   select ' || l_fields        ||
                 '   into :l_result'             ||
                 '   from   ' || p_table_name    ||
                 '   where id = ' || p_id || ';' ||
                 ' end;';

--    logger.debug(p_job_name,M_PACKAGE_NAME,l_prc_name,substr(l_statement, 1, 4000));
    execute immediate l_statement using out l_result;

--    logger.debug(p_job_name,M_PACKAGE_NAME,l_prc_name,l_result);
    return l_result;

  end;



  function write_ni_records
    (p_job_name    in varchar2
    ,p_table_name  in varchar2
    ,p_field_list  in app_utl.t_field_list
    ,p_delimiter   in varchar2
    ,p_handle      in utl_file.file_type) return number is

    cursor     c_stage_error(b_job_name varchar2) is
      select   key_id
      from     stage_error
      where    job_name=b_job_name
      order by key_id;

    l_line  varchar2(4000);
    l_cnt   number := 0;

  begin

     for r_stage_error in c_stage_error(p_job_name)
     loop
       l_line:=get_stage_line
         (p_job_name   => p_job_name
         ,p_table_name => p_table_name
         ,p_id         => r_stage_error.key_id
         ,p_field_list => p_field_list
         ,p_delimiter  => p_delimiter);

       utl_file.put_line(p_handle,l_line);
       l_cnt := l_cnt + 1;
     end loop;
     
     return l_cnt;
  end;



  procedure create_ni_file
    (p_job_name    in varchar2
    ,p_folder      in varchar2
    ,p_filename    in varchar2
    ,p_file_header in varchar2 default null
    ,p_table_name  in varchar2
    ,p_field_list  in app_utl.t_field_list
    ,p_delimiter   in varchar2) is

    l_handle                utl_file.file_type;
    l_prc_name              varchar2(255):='create_ni_file';
    l_cnt number := 0;

  begin

    l_handle:=app_utl.open_file
      (p_folder    => p_folder
      ,p_filename  => p_filename
      ,p_open_mode => 'w');

    if p_file_header is not null then
      write_ni_header
        (p_job_name    => p_job_name
        ,p_handle      => l_handle
        ,p_file_header => p_file_header);
    end if;

    l_cnt := write_ni_records
        (p_job_name    => p_job_name
        ,p_table_name  => p_table_name
        ,p_field_list  => p_field_list
        ,p_delimiter   => p_delimiter
        ,p_handle      => l_handle);

    app_utl.close_file(l_handle,p_filename);
    
    logger.debug(p_job_name, M_PACKAGE_NAME, l_prc_name, 'Nr of records written to NI-file: ' || l_cnt);
  end create_ni_file;



  function get_constraint_info
    (p_job_name        in varchar2
    ,p_constraint_name in varchar2) return user_cons_columns%rowtype is

    l_result              user_cons_columns%rowtype;
    l_prc_name            varchar2(50):='get_constraint_info';

  begin
    select *
      into l_result
      from user_cons_columns
     where constraint_name = upper(p_constraint_name);

    return l_result;

  exception
    when no_data_found then
      logger.error(p_job_name, M_PACKAGE_NAME, l_prc_name, 'no constraint info found for constraint ' || p_constraint_name);
      return null;
  end get_constraint_info;



  function get_primary_key
    (p_job_name   in varchar2
    ,p_table_name in varchar2) return varchar2 is

    l_result         varchar2(256);
    l_prc_name       varchar2(50):='get_primary_key';

  begin
    select constraint_name
      into l_result
      from user_constraints
     where  table_name = upper(p_table_name)
       and constraint_type = 'P';

    logger.debug(p_job_name, M_PACKAGE_NAME, l_prc_name, p_table_name || ' has ' || l_result || ' as primary constraint');
    return l_result;
  exception
    when no_data_found then
      logger.error(p_job_name, M_PACKAGE_NAME, l_prc_name, 'primary constraint not found for table ' || p_table_name);
      return null;
  end get_primary_key;


  function assemble_statement
    (p_job_name         in varchar2
    ,p_table_name       in varchar2
    ,p_error_table_name in varchar2
    ,p_column_name      in varchar2) return varchar2 is

    l_statement         varchar2(4000);
    l_prc_name          varchar2(50):='assemble_statement';
  begin

    l_statement:='insert into stage_error '                       ||
                 '(key_id'                                        ||
                 ',job_name'                                      ||
                 ',table_name'                                    ||
                 ',error_table_name'                              ||
                 ',column_name'                                   ||
                 ',ora_err_number'                                ||
                 ',ora_err_mesg'                                  ||
                 ')'                                              ||
                 'select '                                        ||
                 p_column_name                                    ||
                 ',' || M_QUOTE || p_job_name || M_QUOTE          ||
                 ',' || M_QUOTE || p_table_name || M_QUOTE        ||
                 ',' || M_QUOTE || p_error_table_name || M_QUOTE  ||
                 ',' || M_QUOTE || p_column_name || M_QUOTE       ||
                 ',ora_err_number$'                               ||
                 ',ora_err_mesg$'                                 ||
                 ' from '                                         ||
                 p_error_table_name                               ||
                 ' where job_name = ' || M_QUOTE || p_job_name || M_QUOTE;

    logger.debug(p_job_name, M_PACKAGE_NAME, l_prc_name, l_statement);
    return l_statement;
  end assemble_statement;

  function ins_stage_error
    (p_job_name         in varchar2
    ,p_table_name       in varchar2
    ,p_error_table_name in varchar2
    ,p_column_name      in varchar2) return number is

    pragma autonomous_transaction;

    l_statement            varchar2(4000);
    l_count                number(12);

  begin
    l_statement:=assemble_statement
      (p_job_name         => p_job_name
      ,p_table_name       => p_table_name
      ,p_error_table_name => p_error_table_name
      ,p_column_name      => p_column_name);
    execute immediate l_statement;
    l_count := sql%rowcount;
    commit;

    return l_count;
  end;

  function get_staging_table_fk_field (p_job_name in varchar2
                                      ,p_table_name in varchar2) return varchar2 is
    cursor c_comments(b_table_name varchar2) is
      select c.column_name
      from user_col_comments c
      where c.table_name = upper(b_table_name)
      and upper(c.comments) like 'STAGING_TABLE_ID';
    l_column user_col_comments.column_name%type;
    l_prc_name         varchar2(50):='get_staging_table_fk_field';
  begin
    open c_comments(b_table_name => p_table_name);
      fetch c_comments 
      into l_column;
      if c_comments%found then
        logger.debug(p_job_name, M_PACKAGE_NAME, l_prc_name, 'Staging ID for table '|| p_table_name ||' was found in column ' || l_column);
      end if;
    close c_comments;
    
    return l_column;
  
  end get_staging_table_fk_field;

  function errors
    (p_job_name   in varchar2
    ,p_table_name in varchar2 -- target table!
    ) return number is

    cursor c_constraints(b_primary_key varchar2) is
      select constraint_name
        from user_constraints
       where  constraint_type = 'R'
         and r_constraint_name = b_primary_key;

      l_primary_key       varchar2(256);
      l_count             number(12);
      l_table_name        varchar2(256);
      l_error_table_name  varchar2(256);
      l_column_name       varchar2(256);
      l_stage_column_name varchar2(256) := 'STAGE_ID';
      l_stage_table_name  varchar2(256);
      l_prc_name          varchar2(50):='errors';

    begin
      
      l_error_table_name:=get_error_table(p_job_name, p_table_name);
      l_stage_column_name := get_staging_table_fk_field(p_job_name,p_table_name);
      
      if l_stage_column_name is not null then
        l_count:=ins_stage_error
          (p_job_name         => p_job_name
          ,p_table_name       => p_table_name
          ,p_error_table_name => l_error_table_name
          ,p_column_name      => l_stage_column_name);
      else
        l_primary_key:=get_primary_key(p_job_name, p_table_name);
        l_column_name:=get_constraint_info(p_job_name,l_primary_key).column_name;

        l_count:=ins_stage_error
          (p_job_name         => p_job_name
          ,p_table_name       => p_table_name
          ,p_error_table_name => l_error_table_name
          ,p_column_name      => l_column_name);

        for r_constraint in c_constraints(l_primary_key) loop
          l_table_name:=get_constraint_info(p_job_name,r_constraint.constraint_name).table_name;
          l_error_table_name:=get_error_table(p_job_name,l_table_name);

          -- the table has an error table
          if l_error_table_name is not null then
            l_column_name:=get_constraint_info(p_job_name, r_constraint.constraint_name).column_name;

            l_count:=l_count + ins_stage_error
              (p_job_name         => p_job_name
              ,p_table_name       => p_table_name
              ,p_error_table_name => l_error_table_name
              ,p_column_name      => l_column_name);
          end if;
        end loop;
      end if;

      logger.info(p_job_name, M_PACKAGE_NAME, l_prc_name, l_count || ' error record(s).');
      log_error_records(p_job_name);


      return l_count;
    end errors;

end stager;
/

create or replace package body stager as

  M_QUOTE            constant varchar2(256):=chr(39);
  M_PACKAGE_NAME     constant varchar2(256):=lower($$plsql_unit);

  M_TAB              constant varchar2(1):=chr(9);

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

  begin
    l_fields:=app_utl.field_list_to_varchar
      (p_field_list => p_field_list
      ,p_delimiter  => ',');

    l_statement:='insert into ' || p_stage_table_name                ||
                 '(id '                                              ||  
                 ',file_id '                                         ||                
                 ',row_id '                                          ||
                 ',job_name '                                        ||
                 ',' || l_fields                                     ||
                 ')'                                                 ||
                 ' select ' || p_stage_table_name || '_s.nextval'    ||      
                          ',' || p_file_id                           ||               
                          ',rownum'                                  ||
                          ',' || M_QUOTE ||  p_job_name || M_QUOTE   ||
                          ',' || l_fields                            ||
                 ' from   ' || p_table_name                          ||
                 ' log errors into ' || p_stage_table_name || '_err' ||
                 ' reject limit unlimited';

    logger.debug(p_job_name,M_PACKAGE_NAME,l_prc_name,substr(l_statement, 1, 4000));
    execute immediate l_statement;
    l_count:=SQL%ROWCOUNT;
    commit;
    logger.info(p_job_name,M_PACKAGE_NAME,l_prc_name,l_count || ' records(s) staged.');
    return l_count;

  end;

  procedure log_error_records
    (p_job_name in varchar2
    ,p_type     in varchar2 default G_TYPE_ERROR) is

    cursor     c_stage_result(b_job_name varchar2) is
      select   id, info
      from     stage_result
      where    type=p_type
      and      job_name=b_job_name
      order by id;

    l_prc_name  varchar2(255):='log_error_records';

  begin

    for r_stage_result in c_stage_result(p_job_name)
    loop
      logger.error(p_job_name,M_PACKAGE_NAME,l_prc_name,r_stage_result.id || ' ' || r_stage_result.info);
    end loop;

  end;


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
            ,format_error_backtrace
            ,created_at
            ,created_by
      from   log
      where  job_name=b_job_name;

    r_log     c_log%rowtype;
    l_line    varchar2(32000);

  begin
    for r_log in c_log(p_job_name)
    loop
      l_line:=to_char(r_log.created_at,'dd/mm/yyyy hh24:mi:ss')  || M_TAB ||
              r_log.created_by                                   || M_TAB ||
              r_log.logtype_code                                 || M_TAB ||
              '[' || lower(r_log.package_name) || '.' || lower(r_log.method_name) || ']' || M_TAB ||
              r_log.message     || M_TAB ||
              r_log.format_error_backtrace || M_TAB;

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

    l_handle:=app_utl.open_file(p_folder    => p_folder
                               ,p_filename  => p_filename
                               ,p_open_mode => 'w');

    write_log_records(p_job_name,l_handle);

    app_utl.close_file(l_handle,p_filename);
  end;



  procedure write_ni_header
    (p_job_name    in varchar2
    ,p_handle      in utl_file.file_type
    ,p_file_header in varchar2) is
  begin
     utl_file.put_line(p_handle,p_file_header);
  end;


  procedure write_ni_records
    (p_job_name in varchar2
    ,p_handle in utl_file.file_type
    ,p_type     in varchar2 default G_TYPE_NI) is

    cursor     c_stage_result(b_job_name varchar2) is
      select   id, info
      from     stage_result
      where    type=p_type
      and      job_name=b_job_name
      order by id;

  begin

     for r_stage_result in c_stage_result(p_job_name)
     loop
       utl_file.put_line(p_handle,r_stage_result.info);
     end loop;

  end;


  procedure create_ni_file
    (p_job_name    in varchar2
    ,p_folder      in varchar2
    ,p_filename    in varchar2
    ,p_file_header in varchar2 default null
    ,p_type        in varchar2 default G_TYPE_NI) is


    l_handle                utl_file.file_type;
    l_prc_name              varchar2(255):='create_ni_file';

  begin

    l_handle:=app_utl.open_file(p_folder    => p_folder
                               ,p_filename  => p_filename
                               ,p_open_mode => 'w');

    if p_file_header is not null then
      write_ni_header(p_job_name,l_handle,p_file_header);
    end if;

    write_ni_records(p_job_name,l_handle,p_type);

    app_utl.close_file(l_handle,p_filename);
  end;



  function ins_stage_result
    (p_job_name          in varchar2
    ,p_err_table_name    in varchar2
    ,p_stage_table_name  in varchar2
    ,p_fields            in varchar2
    ,p_type              in varchar2) return number is

    l_prc_name       varchar2(4000):='ins_stage_result';
    l_statement      varchar2(32000);
    l_count          number(12):=0;


  begin
    l_statement:='insert into stage_result '                      ||
                 '(id,type,job_name,info) '                  ||
                 'select '                                   ||
                 '  l.row_id,'                               ||
                    M_QUOTE || p_type || M_QUOTE || ','      ||
                    M_QUOTE || p_job_name || M_QUOTE ||  ',' ||
                    p_fields                                 ||
                 ' from '                                    ||
                    p_err_table_name || ' e, '               ||
                    p_stage_table_name || ' l '               ||
                 ' where e.row_id=l.row_id '                 ||
                 ' and e.job_name=l.job_name '               ||
                 ' and e.job_name=' || M_QUOTE || p_job_name || M_QUOTE;

    logger.debug(p_job_name, M_PACKAGE_NAME, l_prc_name, substr(l_statement, 1, 4000));
    execute immediate l_statement;
    l_count := sql%rowcount;

    return l_count;
  end;


  function prepare_error_records
    (p_job_name          in varchar2
    ,p_err_table_name    in varchar2
    ,p_stage_table_name  in varchar2
    ,p_field_list        in app_utl.t_field_list
    ,p_type              in varchar2 default G_TYPE_ERROR) return number is

    l_prc_name  varchar2(255):='prepare_error_records';
    l_fields    varchar2(4000);
    l_count     number(12);

  begin

    l_fields:=app_utl.field_list_to_varchar
      (p_field_list => p_field_list
      ,p_delimiter  => '|');

    l_fields:=app_utl.column_character_before
      (p_columns => l_fields
      ,p_column_delimiter => '|'
      ,p_character        => 'l.');

    l_fields:='e.ORA_ERR_MESG$|' || l_fields;

    l_fields:=app_utl.get_sql_one_column
      (p_column_names => l_fields
      ,p_column_delimiter => '|');

    l_count:=ins_stage_result
    (p_job_name          => p_job_name
    ,p_err_table_name    => p_err_table_name
    ,p_stage_table_name  => p_stage_table_name
    ,p_fields            => l_fields
    ,p_type              => p_type);

    return l_count;
  end;


  function prepare_ni_records
    (p_job_name          in varchar2
    ,p_err_table_name    in varchar2
    ,p_stage_table_name  in varchar2
    ,p_field_list        in app_utl.t_field_list
    ,p_type              in varchar2 default G_TYPE_NI) return number is

    l_prc_name  varchar2(255):='prepare_ni_records';
    l_fields    varchar2(4000);
    l_count     number(12);

  begin

    l_fields:=app_utl.field_list_to_varchar
      (p_field_list => p_field_list
      ,p_delimiter  => '|');

    l_fields:=app_utl.column_character_before
      (p_columns => l_fields
      ,p_column_delimiter => '|'
      ,p_character        => 'l.');

    l_fields:=app_utl.get_sql_one_column
      (p_column_names => l_fields
      ,p_column_delimiter => '|');

    l_count:=ins_stage_result
    (p_job_name          => p_job_name
    ,p_err_table_name    => p_err_table_name
    ,p_stage_table_name  => p_stage_table_name
    ,p_fields            => l_fields
    ,p_type              => p_type);

    return l_count;

  end;


  function ins_stage_result
    (p_job_name          in varchar2
    ,p_stage_table_name  in varchar2
    ,p_fields            in varchar2
    ,p_type              in varchar2) return number is

    l_prc_name       varchar2(4000):='ins_stage_result';
    l_statement      varchar2(32000);
    l_count          number(12):=0;


  begin
    l_statement:='insert into stage_result '                     ||
                 '(id,type,job_name,info) '                 ||
                 'select '                                  ||
                 '  row_id,'                                ||
                    M_QUOTE || p_type || M_QUOTE || ','     ||
                    M_QUOTE || p_job_name || M_QUOTE || ',' ||
                    p_fields                                ||
                 ' from ' || p_stage_table_name || '_err'    ||
                 ' where job_name=' || M_QUOTE || p_job_name || M_QUOTE;

    logger.debug(p_job_name, M_PACKAGE_NAME, l_prc_name, substr(l_statement, 1, 4000));
    execute immediate l_statement;
    l_count := sql%rowcount;

    return l_count;
  end;


  function prepare_error_records
    (p_job_name          in varchar2
    ,p_stage_table_name   in varchar2
    ,p_field_list        in app_utl.t_field_list) return number is

    l_prc_name  varchar2(255):='prepare_error_records';
    l_fields    varchar2(4000);
    l_count     number(12);

  begin

    l_fields:=app_utl.field_list_to_varchar
      (p_field_list => p_field_list
      ,p_delimiter  => '|');

    l_fields:='ORA_ERR_MESG$|' || l_fields;

    l_fields:=app_utl.get_sql_one_column
      (p_column_names => l_fields
      ,p_column_delimiter => '|');

    l_count:=ins_stage_result
    (p_job_name          => p_job_name
    ,p_stage_table_name  => p_stage_table_name
    ,p_fields            => l_fields
    ,p_type              => G_TYPE_ERROR);

    return l_count;

  end;


  function prepare_ni_records
    (p_job_name          in varchar2
    ,p_stage_table_name  in varchar2
    ,p_field_list        in app_utl.t_field_list
    ,p_type              in varchar2 default G_TYPE_NI) return number is

    l_prc_name  varchar2(255):='prepare_ni_records';
    l_fields    varchar2(4000);
    l_count     number(12);

  begin

    l_fields:=app_utl.field_list_to_varchar
      (p_field_list => p_field_list
      ,p_delimiter  => '|');

    l_fields:=app_utl.get_sql_one_column
      (p_column_names => l_fields
      ,p_column_delimiter => '|');

    l_count:=ins_stage_result
    (p_job_name          => p_job_name
    ,p_stage_table_name  => p_stage_table_name
    ,p_fields            => l_fields
    ,p_type              => p_type);

    return l_count;

  end;



  function ins_stage_result
    (p_job_name          in varchar2
    ,p_table_name        in varchar2
    ,p_err_table_name    in varchar2
    ,p_fields            in varchar2
    ,p_type              in varchar2) return number is

    l_prc_name       varchar2(4000):='ins_stage_result';
    l_statement      varchar2(32000);
    l_count          number(12):=0;


  begin
    l_statement:='insert into stage_result '                     ||
                 '(id,type,job_name,info) '                      ||
                 'select '                                       ||
                 '  l.row_id,'                                   ||
                    M_QUOTE || p_type || M_QUOTE || ','          ||
                    M_QUOTE || p_job_name || M_QUOTE ||  ','     ||
                    p_fields                                     ||
                 ' from '                                        ||
                    p_err_table_name || ' e, '                   ||
                    p_table_name     || ' l  '                   ||
                 ' where e.row_id   = l.id '                     ||
                 '   and e.job_name = ' || M_QUOTE || p_job_name || M_QUOTE;

    logger.debug(p_job_name, M_PACKAGE_NAME, l_prc_name, substr(l_statement, 1, 4000));
    execute immediate l_statement;
    l_count := sql%rowcount;

    return l_count;
  end;



  function prepare_error_records
    (p_job_name          in varchar2
    ,p_table_name        in varchar2
    ,p_err_table_name    in varchar2) return number is

    l_prc_name  varchar2(255):='prepare_error_records';
    l_fields    varchar2(4000);
    l_count     number(12);
    l_field_list        app_utl.t_field_list;

  begin

    l_field_list:=app_utl.get_field_list_of_table
      (p_table_name => p_table_name);

    l_fields:=app_utl.field_list_to_varchar
      (p_field_list => l_field_list
      ,p_delimiter  => '|');

    l_fields:=app_utl.column_character_before
      (p_columns => l_fields
      ,p_column_delimiter => '|'
      ,p_character        => 'l.');

    l_fields:='e.ORA_ERR_MESG$|' || l_fields;

    l_fields:=app_utl.get_sql_one_column
      (p_column_names => l_fields
      ,p_column_delimiter => '|');

    l_count:=ins_stage_result
    (p_job_name        => p_job_name
    ,p_table_name      => p_table_name
    ,p_err_table_name  => p_err_table_name
    ,p_fields          => l_fields
    ,p_type            => G_TYPE_ERROR);

    return l_count;
  end;


  function prepare_dbl_error_records
    (p_job_name          in varchar2
    ,p_table_name        in varchar2
    ,p_dblink            in varchar2
    ,p_err_table_name    in varchar2) return number is

    l_prc_name  varchar2(255):='prepare_dbl_error_records';
    l_fields    varchar2(4000);
    l_count     number(12);
    l_field_list        app_utl.t_field_list;

  begin

    l_field_list:=app_utl.get_field_list_of_dbl_table
      (p_table_name => p_table_name
      ,p_dblink     => p_dblink);

    l_fields:=app_utl.field_list_to_varchar
      (p_field_list => l_field_list
      ,p_delimiter  => '|');

    l_fields:=app_utl.column_character_before
      (p_columns => l_fields
      ,p_column_delimiter => '|'
      ,p_character        => 'l.');

    l_fields:='e.ORA_ERR_MESG$|' || l_fields;

    l_fields:=app_utl.get_sql_one_column
      (p_column_names => l_fields
      ,p_column_delimiter => '|');

    l_count:=ins_stage_result
    (p_job_name        => p_job_name
    ,p_table_name      => p_table_name
    ,p_err_table_name  => p_err_table_name
    ,p_fields          => l_fields
    ,p_type            => G_TYPE_ERROR);

    return l_count;
  end;



  function ins_stage_result
    (p_job_name          in varchar2
    ,p_err_table_name    in varchar2
    ,p_fields            in varchar2
    ,p_type              in varchar2) return number is

    l_prc_name       varchar2(4000):='ins_stage_result';
    l_statement      varchar2(32000);
    l_count          number(12):=0;


  begin

    l_statement:='insert into stage_result '                     ||
                 '(id,type,job_name,info) '                      ||
                 'select '                                       ||
                 '  e.row_id,'                                   ||
                    M_QUOTE || p_type || M_QUOTE || ','          ||
                    M_QUOTE || p_job_name || M_QUOTE ||  ','     ||
                 '  e.ORA_ERR_MESG$'                             ||
                 ' from '                                        ||
                    p_err_table_name || ' e '                    ||
                 ' where e.job_name   = ' || M_QUOTE || p_job_name || M_QUOTE;

    logger.debug(p_job_name, M_PACKAGE_NAME, l_prc_name, substr(l_statement, 1, 4000));
    execute immediate l_statement;
    l_count := sql%rowcount;

    return l_count;
  end;



  function prepare_error_records
    (p_job_name          in varchar2
    ,p_err_table_name    in varchar2) return number is

    l_prc_name  varchar2(255):='prepare_error_records';
    l_fields    varchar2(4000);
    l_count     number(12);
    l_field_list        app_utl.t_field_list;

  begin

    l_fields:='e.ORA_ERR_MESG$';

    l_count:=ins_stage_result
    (p_job_name        => p_job_name
    ,p_err_table_name  => p_err_table_name
    ,p_fields          => l_fields
    ,p_type            => G_TYPE_ERROR);

    return l_count;
  end;

end stager;
/
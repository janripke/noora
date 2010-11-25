create or replace package body app_utl as

  M_QUOTE            constant varchar2(256):=chr(39);
  M_PACKAGE_NAME     constant varchar2(256):=upper($$plsql_unit);
  M_YES              constant varchar2(1):='Y';
  M_NO_ROWS          constant varchar2(255):='NO ROWS';
  M_LF               constant varchar2(1):=chr(10);
  M_CR               constant varchar2(1):=chr(13);


  function xx_length(p_value in varchar2) return number is

    l_result  number(12):=0;

  begin
	if p_value is null then
	  l_result:=0;
	else
	  l_result:=length(p_value);
	end if;

	return l_result;
  end;


  function get_random_number(p_length in number) return varchar2 is

    l_result  varchar2(255);

  begin
    l_result:=replace(to_char(floor(dbms_random.value*power(10,p_length)),'0999'),' ','');
    return l_result;
  end;

  function get_field_list(p_fields in varchar2, p_fieldtypes in varchar2, p_delimiter in varchar2) return t_field_list is
    l_field_list     t_field_list;
    l_field          t_field;
    l_field_count    integer;
  begin

    l_field_count:=get_column_count(p_fields,';');
    for i in 1..l_field_count
    loop
      l_field.name:=get_column(p_fields,';',i);
      l_field.type:=get_column(p_fieldtypes,';',i);
      l_field_list(l_field_list.count):=l_field;
    end loop;

    return l_field_list;
  end;


  function get_field_list_of_table
    (p_table_name in varchar2) return t_field_list is

    cursor c_columns(b_table_name varchar2) is
      select column_name
           , data_type
           , data_length
           , data_precision
           , data_scale
      from   user_tab_columns
      where table_name=upper(p_table_name)
      order by column_id;

    l_field_list    t_field_list;
    l_field         t_field;
    r_columns       c_columns%rowtype;

  begin
    for r_columns in c_columns(p_table_name)
    loop
      l_field.name:=r_columns.column_name;
      if r_columns.data_type='NUMBER' then
        l_field.type:=r_columns.data_type ||
                      '(' ||
                      r_columns.data_precision ||
                      ',' ||
                      r_columns.data_scale ||
                      ')';
      elsif r_columns.data_type='VARCHAR2' then
        l_field.type:=r_columns.data_type ||
                      '(' ||
                      r_columns.data_length ||
                      ')';
      else
        l_field.type:=r_columns.data_type;
      end if;

      l_field_list(l_field_list.count):=l_field;

    end loop;

    return l_field_list;

  end;

  
  function get_field_list_of_dbl_table
  (
    p_table_name in varchar2
   ,p_dblink     in varchar2
  ) return t_field_list is
  /* robst
  Use dynamic query with dblink supplied by p_dblink
  */
  
    l_field_list t_field_list;
    l_field      t_field;

    l_select         varchar2(4000);
    l_column_name    user_tab_columns.column_name%type;
    l_data_type      user_tab_columns.data_type%type;
    l_data_length    user_tab_columns.data_length%type;
    l_data_precision user_tab_columns.data_precision%type;
    l_data_scale     user_tab_columns.data_scale%type;
    type t_refcur    is ref cursor;
    r_cols           t_refcur;
  
  begin
    -- Mind the use of spaces while composing dyn SQL!
    -- Mind that ''' results in '
    l_select := '
      select column_name name
      ,case data_type
       when ''NUMBER'' then data_type || ''('' || data_precision || '','' || data_scale || '')''
       when ''VARCHAR2'' then data_type || ''('' || data_length || '')''
       else data_type
       end type
      from   user_tab_columns@' || p_dblink ||
                ' where table_name=''' || upper(p_table_name) ||
                ''' order by column_id';
                
    open r_cols for l_select;
    loop
      fetch r_cols
        into l_field;
      exit when r_cols%notfound;

      l_field_list(l_field_list.count) := l_field;
          
    end loop;
    close r_cols;
  
    return l_field_list;
  
  end get_field_list_of_dbl_table;

  function get_field_list_of_varchar256(p_fields in varchar2, p_delimiter in varchar2) return t_field_list is
    l_field_list     t_field_list;
    l_field          t_field;
    l_field_count    integer;
  begin

    l_field_count:=get_column_count(p_fields,p_delimiter);
    for i in 1..l_field_count
    loop
      l_field.name:=get_column(p_fields,p_delimiter,i);
      l_field.type:='varchar2(256)';
      l_field_list(l_field_list.count):=l_field;
    end loop;

    return l_field_list;
  end;
  
  
  function get_field_list_of_varchar4000
    (p_fields in varchar2
	,p_delimiter in varchar2) return t_field_list is
		
    l_field_list     t_field_list;
    l_field          t_field;
    l_field_count    integer;
  begin

    l_field_count:=get_column_count(p_fields,p_delimiter);
    for i in 1..l_field_count
    loop
      l_field.name:=get_column(p_fields,p_delimiter,i);
      l_field.type:='varchar2(4000)';
      l_field_list(l_field_list.count):=l_field;
    end loop;

    return l_field_list;
  end;


  function field_list_to_varchar
    (p_field_list in t_field_list
    ,p_delimiter  in varchar2) return varchar2 is

    l_count      number(12);
    l_field      t_field;
    l_result     varchar2(4000);
    --l_result     varchar2(8000);  -- robst

  begin
    l_count:=p_field_list.count;
    for i in 0..l_count-1 loop
      l_field:=p_field_list(i);
      l_result:=l_result || l_field.name || p_delimiter;
    end loop;
    l_result:=rtrim(l_result,p_delimiter);
    return l_result;
  end;



  function get_job_name(p_prefix varchar2) return varchar2 is
  begin
    return dbms_scheduler.generate_job_name(p_prefix);
  end;


  function get_oracle_folder(p_directory_name in varchar2) return varchar2 is

    l_folder  varchar2(255);

  begin
    select directory_path
    into   l_folder
    from   all_directories
    where  directory_name=p_directory_name;

    return l_folder;
  end;
  
  
  function join
    (p_collection in t_collection
    ,p_delimiter  in varchar2) return varchar2 is

    l_count      number(12);
    l_value      varchar2(4000);
    l_result     varchar2(4000);
    --l_result     varchar2(8000);  -- robst

  begin
    l_count:=p_collection.count;
    for i in 0..l_count-1 loop
      l_value:=p_collection(i);
      l_result:=l_result || l_value || p_delimiter;
    end loop;
    l_result:=rtrim(l_result,p_delimiter);
    return l_result;
  end;


  function split(s in varchar2, delimiter in varchar2) return t_collection is
    l_collection    t_collection;
    start_position  integer := 1;
    position        integer := 0;
  begin
    while position < length(s)
    loop
      position := instr(s, delimiter, start_position);

      if position = 0 then
        position := length(s) + 1;
      end if;

      l_collection(l_collection.count + 1) := substr(s, start_position, position - start_position);
      start_position := position + 1;
    end loop;

    return l_collection;
  end;


  function get_column_count(p_string in varchar2, p_delimiter in varchar2) return integer is
    l_collection t_collection;
  begin
    l_collection := split(p_string, p_delimiter);
    return l_collection.count;
  end;


  function get_column(p_string in varchar2, p_delimiter in varchar2, p_column in integer) return varchar2 is
    l_collection t_collection;
  begin
    l_collection := split(p_string, p_delimiter);
    if p_column <= l_collection.count then
      return l_collection(p_column);
    else
      return null;
    end if;
  end;
  
 

  function file_header_is_valid(p_job_name in varchar2
                               ,p_folder in varchar2
                               ,p_filename in varchar2
                               ,p_file_header in varchar2) return boolean is

    l_handle utl_file.file_type;
    l_line   varchar2(4000);
    l_result boolean:=false;
    l_prc_name  varchar2(255):='file_header_is_valid';

  begin
    logger.debug(p_job_name,M_PACKAGE_NAME,l_prc_name,'file header in db:' || p_file_header);
    l_handle:=app_utl.open_file(p_folder    => p_folder
                               ,p_filename  => p_filename
                               ,p_open_mode => 'r');
    utl_file.get_line(l_handle,l_line);

    -- l_line := rtrim(l_line, M_LF); -- MCP-96 : header validatie - strip newline characters uit fileheader
    -- l_line := rtrim(l_line, M_CR); -- MCP-96 : header validatie - strip newline characters uit fileheader

    l_line := replace(l_line,M_LF,''); -- MCP-96 : header validatie - strip newline characters uit fileheader
    l_line := replace(l_line,M_CR,''); -- MCP-96 : header validatie - strip newline characters uit fileheader


    logger.debug(p_job_name,M_PACKAGE_NAME,l_prc_name,'file header in file :'|| l_line);
    if lower(l_line)=lower(p_file_header) then
      l_result:=true;
    end if;
    app_utl.close_file(l_handle,p_filename);

    return l_result;

  end;


  function open_file(p_folder        in varchar2
                    ,p_filename      in varchar2
                    ,p_open_mode     in varchar2
                    ,p_max_linesize  in number default 32000) return utl_file.file_type is

    l_handle  utl_file.file_type;

  begin
    if (not utl_file.is_open(l_handle)) then

      l_handle:=utl_file.fopen(location => p_folder
                              ,filename => p_filename
                              ,open_mode => p_open_mode
                              ,max_linesize => p_max_linesize);

    end if;
    return l_handle;

  exception
    when utl_file.invalid_path then
      raise_application_error(-20999,'invalid folder (' || p_folder || ', ' || p_filename || ')');
    when utl_file.invalid_mode then
      raise_application_error(-20999,'invalid mode (' || p_open_mode || ', ' || p_filename || ')');
    when utl_file.invalid_filehandle then
      raise_application_error(-20999,'invalid handle (' || p_filename || ')');
    when utl_file.invalid_operation then
      raise_application_error(-20999,'invalid operation (' || p_folder || ', ' || p_filename || ')');
    when utl_file.read_error then
      raise_application_error(-20999,'read error (' || p_filename || ')');
    when utl_file.write_error then
      raise_application_error(-20999,'write error (' || p_filename || ')');
    when utl_file.internal_error then
      raise_application_error(-20999,'internal error (' || p_filename || ')');
    when others then
      raise_application_error(-20999,'unknown error (' || sqlcode || ', ' || p_filename || ', ' || sqlerrm || ')');
  end;


  procedure close_file(p_handle   in out utl_file.file_type
                      ,p_filename in varchar2) is
					  	
  l_prc_name  varchar2(50):='close_file';						
						
  begin
    if utl_file.is_open(p_handle) then
      utl_file.fclose(p_handle);
    end if;
  exception
    when others then
      raise_application_error(-20999,'unknown error (' || sqlcode || ', ' || p_filename || ', ' || sqlerrm || ')');
  end;


  function prepare_create_table(p_job_name in varchar2, p_tablename in varchar2, p_field_list in t_field_list) return varchar2 is
    l_count       integer;
    l_field       t_field;
    --l_result      varchar2(4096);      
    l_result      varchar2(8000);  -- robst
    l_prc_name    varchar2(255):='prepare_create_table';
  begin
    l_result:='create table ' || p_tablename || ' (';
    l_count:=p_field_list.count;
    for i in 0..l_count-1 loop
      l_field:=p_field_list(i);
      l_result:=l_result || l_field.name || ' ' || l_field.type || ',';
    end loop;
    l_result:=rtrim(l_result,',') || ')';
    return l_result;
  end;


  function get_skip_header(p_skip_header_yn in varchar2) return varchar2 is

    l_result  varchar2(255):='';

  begin
    if upper(p_skip_header_yn)=M_YES then
      l_result:='skip 1';
    end if;
    return l_result;
  end;


  function get_sql_one_column
    (p_column_names in varchar2
    ,p_column_delimiter in varchar2) return varchar2 is

    l_columns  varchar2(4000);

  begin
   l_columns := replace(p_column_names, p_column_delimiter, '||' || M_QUOTE || p_column_delimiter || M_QUOTE || '||');
   return l_columns;
  end;


  function column_character_before
    (p_columns          in varchar2
    ,p_column_delimiter in varchar2
    ,p_character        in varchar2) return varchar2 is

    l_count   number(12);
    l_column  varchar2(255);
    l_result  varchar2(4000);

  begin
    l_count:= get_column_count(p_columns,p_column_delimiter);
    for i in 1..l_count loop
      l_column:=get_column(p_columns,p_column_delimiter,i);
      l_result:=l_result || p_character || l_column || p_column_delimiter;
    end loop;
    return rtrim(l_result,p_column_delimiter);
  end;


  function table_present
    (p_table_name in varchar2) return boolean is

    l_count   number(12);
    l_result  boolean:=false;
  begin
    select count(0)
    into l_count
    from user_tables
    where table_name=p_table_name;

    if l_count<>0 then
      l_result:=true;
    end if;

    return l_result;
  end;


  function table_not_present
    (p_table_name in varchar2) return boolean is

    l_count   number(12);
    l_result  boolean:=true;
  begin
    select count(0)
    into l_count
    from user_tables
    where table_name=p_table_name;

    if l_count<>0 then
      l_result:=false;
    end if;

    return l_result;
  end;


  function prepare_create_sequence
    (p_sequence_name in varchar2) return varchar2 is

    l_result  varchar2(1024);
  begin
    l_result:='create sequence ' || p_sequence_name ||
              ' minvalue 1 '            ||
              ' maxvalue 999999999999 ' ||
              ' start with 1 '          ||
              ' increment by 1 '        ||
              ' nocache ';
    return l_result;
  end;


  procedure create_sequence
    (p_job_name in varchar2
    ,p_sequence_name in varchar2) is

    pragma autonomous_transaction;

    l_statement   varchar2(4000);
    l_prc_name    varchar2(255):='create_sequence';
  begin
    l_statement:=prepare_create_sequence(p_sequence_name);
    logger.debug(p_job_name,M_PACKAGE_NAME,l_prc_name,substr(l_statement,1,4000));
    execute immediate l_statement;
  end;


  procedure create_table
  (p_job_name   in varchar2
  ,p_table_name in varchar2
  ,p_field_list in app_utl.t_field_list) is

    pragma autonomous_transaction;

    l_statement   varchar2(8000);
    l_prc_name    varchar2(255):='create_table';
  begin
    l_statement:=prepare_create_table(p_job_name,p_table_name,p_field_list);
    logger.debug(p_job_name,M_PACKAGE_NAME,l_prc_name,substr(l_statement,1,4000));
    execute immediate l_statement;
  end;


  function get_records_delimited_by
    (p_job_name in varchar2
    ,p_folder   in varchar2
    ,p_filename in varchar2) return varchar2 is

    l_handle   utl_file.file_type;
    l_buffer   raw(32767);
    l_result   varchar2(50):='newline';
    l_prefix   varchar2(50):='records delimited by ';
    l_prc_name    varchar2(255):='get_records_delimited_by';

  begin
    l_handle:=open_file(p_folder,p_filename,'rb',32767);
    utl_file.get_raw(l_handle,l_buffer, 32767);
    close_file(l_handle,p_filename);

    if instr(l_buffer,'0D0A')>0 then
      l_result:=M_QUOTE || '\r\n' || M_QUOTE;
    elsif instr(l_buffer,'0A')>0 then
      l_result:=M_QUOTE || '\n' || M_QUOTE;
    elsif instr(l_buffer,'0D')>0 then
      l_result:=M_QUOTE || '\r' || M_QUOTE;
    end if;

    return l_prefix || l_result;
  exception
  	when NO_DATA_FOUND then
      logger.warn(p_job_name,M_PACKAGE_NAME,l_prc_name,M_NO_ROWS);
  	  return l_prefix || l_result;
  end;


  procedure create_error_table
    (p_job_name       in varchar2
    ,p_table_name     in varchar2
    ,p_err_table_name in varchar2) is

    pragma autonomous_transaction;

    l_prc_name     varchar2(50):='create_error_table';

  begin
    dbms_errlog.create_error_log(p_table_name,p_err_table_name);
    logger.debug(p_job_name,M_PACKAGE_NAME,l_prc_name,'error table ' || p_err_table_name || ' created' );
  end;


  function get_optionally_enclosed(p_optionally_enclosed_yn in varchar2) return varchar2 is
  
    l_result varchar2(255):='';
    
  begin
    if upper(p_optionally_enclosed_yn)=M_YES then
      l_result:= ' optionally enclosed by ''"'' ';
    end if;
    return l_result;
  end;

  
  procedure create_external_table
    (p_job_name               in varchar2
    ,p_folder                 in varchar2
    ,p_filename               in varchar2
    ,p_tablename              in varchar2
    ,p_skip_header_yn         in varchar2
    ,p_field_delimiter        in varchar2
    ,p_optionally_enclosed_yn in varchar2 default 'N'
    ,p_field_list             in t_field_list) is

  pragma autonomous_transaction;

  l_statement   varchar2(32000);
  l_filename    varchar2(256);
  l_prc_name    varchar2(255):='create_external_table';

  begin
    l_filename:=get_column(p_filename,'.',1);
    l_statement:=prepare_create_table(p_job_name, p_tablename,p_field_list) || '
                  organization external(
                    type oracle_loader
                    default directory ' || p_folder || '
                    access parameters ( ' ||
                      get_records_delimited_by(p_job_name,p_folder,p_filename) || ' '||
                      get_skip_header(p_skip_header_yn) ||
                      'BADFILE ' || M_QUOTE || l_filename || '.bad' || M_QUOTE || '
                      LOGFILE ' || M_QUOTE || l_filename || '.log' || M_QUOTE || '
                      fields terminated by ' || M_QUOTE || p_field_delimiter || M_QUOTE ||
                      get_optionally_enclosed(p_optionally_enclosed_yn ) || 
                      ' missing field values are null
                    )
                    location (' || M_QUOTE || p_filename || M_QUOTE || ')
                  )
                  parallel
                  reject limit unlimited';
    logger.debug(p_job_name,M_PACKAGE_NAME,l_prc_name,substr(l_statement,1,4000));
    execute immediate l_statement;
  end;
  
  

  procedure drop_external_table(p_job_name in varchar2, p_tablename in varchar2) is
    l_statement   varchar2(4096);
    l_prc_name    varchar2(255):='drop_external_table';

  pragma autonomous_transaction;

  begin
    l_statement:='drop table ' || p_tablename;
    execute immediate l_statement;

  exception
    when others then
      logger.warn(p_job_name,M_PACKAGE_NAME,l_prc_name,'could not drop external table '|| p_tablename);
  end drop_external_table;


  function nnvl
    (p_value in varchar2
    ,p_replacement in varchar2) return VARCHAR2 is
  begin
    if p_value is not null then
      return p_replacement;
    end if;

    return p_value;

  end nnvl;
  
  procedure write_blob_to_file
    (p_job_name    in varchar2
	,p_folder      in varchar2
    ,p_filename    in varchar2
    ,p_content     in blob) is
    
    l_blob_length       number(12);
    l_clob_length       number(12);    
    l_handle            utl_file.file_type;
	l_prc_name          varchar2(256) := 'write_blob_to_file';
    l_buffer_size       constant binary_integer := 32767;
    l_offset            number(12):=1;
    l_length            number(12):=0;
    l_amount            binary_integer;
    l_buffer            raw(32767);
    
  begin

    l_handle:=app_utl.open_file
      (p_folder        => p_folder
      ,p_filename      => p_filename
      ,p_open_mode     => 'W');
 
    l_length:=dbms_lob.getlength(p_content);
    while l_offset<(l_length+1) loop
      l_amount:=l_buffer_size;
      dbms_lob.read(p_content,l_amount,l_offset,l_buffer);
      utl_file.put_raw(file => l_handle, buffer => l_buffer  , autoflush => TRUE);
      l_offset:=l_offset+l_amount;
    end loop;

    app_utl.close_file(p_handle   => l_handle
                      ,p_filename => p_filename);
                     
    logger.info(p_job_name,M_PACKAGE_NAME,l_prc_name,'file '|| p_filename || ' created from BLOB');   				  
                      
  end write_blob_to_file;
  
  
  function to_date_
    (p_value  in varchar2
    ,p_format in varchar2) return date is
        
    l_result date;
  begin
    select to_date(p_value,p_format)
      into l_result
      from dual;
    return l_result;
  exception
    when others
    then
      raise_application_error(E_INVALID_DATE,sqlerrm);
  end;
  
 
  
  function to_timestamp_tz_
    (p_value  in varchar2
    ,p_format in varchar2) return timestamp with time zone is
        
    l_result timestamp with time zone;
  begin
    select to_timestamp_tz(p_value,p_format)
      into l_result
      from dual;
    return l_result;
  exception
    when others
    then
      raise_application_error(E_INVALID_TIMESTAMP_TZ,sqlerrm);
  end;
  
  
  
  function to_timestamp_
    (p_value  in varchar2
    ,p_format in varchar2) return timestamp is
        
    l_result timestamp;
  begin
    select to_timestamp(p_value,p_format)
      into l_result
      from dual;
    return l_result;
  exception
    when others
    then
      raise_application_error(E_INVALID_TIMESTAMP,sqlerrm);
  end;
  
  
  function to_number_
    (p_value       in varchar2) return number is
        
    l_result number;
  begin
    select to_number(p_value)
      into l_result
      from dual;
    return l_result;
  exception
    when others
    then
      raise_application_error(E_INVALID_NUMBER,sqlerrm);
  end;
                 

  function get_index
    (p_collection in t_collection, p_name in varchar2) return number is

    l_count      number(12);
    l_field      t_field;

  begin
    l_count:=p_collection.count;
    for i in 0..l_count-1 loop
      if p_collection(i)=p_name then
        return i;
      end if;
    end loop;
    return null;
  end;

  
  function get_directory_details
    (p_directory_name  in varchar2) return all_directories%rowtype is

    cursor c_dir(b_directory_name varchar2) is
      select *
      from   all_directories
      where  directory_name = b_directory_name;

    r_dir  c_dir%rowtype;

  begin
    open  c_dir(p_directory_name);
    fetch c_dir into r_dir;
    close c_dir;
    return r_dir;
  end get_directory_details;


end app_utl;
/

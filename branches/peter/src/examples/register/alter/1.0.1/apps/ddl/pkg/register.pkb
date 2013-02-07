create or replace package body register is

  M_PACKAGE_NAME               constant varchar2(256):=lower($$plsql_unit);

  function ins_file
    (p_file     in files%rowtype) return files%rowtype is

    l_prc_name varchar2(255) := 'ins_file';
    l_file     files%rowtype:=p_file;
    l_id       number(12);

  begin

    insert into files
      (job_name
      ,filename
      ,filetype
      ,status_code
      ,records_total
      ,records_ok
      ,records_error
      ,records_ignored
      ,external_id)
    values
      (p_file.job_name
      ,p_file.filename
      ,p_file.filetype
      ,p_file.status_code
      ,nvl(p_file.records_total,0)
      ,nvl(p_file.records_ok,0)
      ,nvl(p_file.records_error,0)
      ,nvl(p_file.records_ignored,0)
      ,p_file.external_id)
    returning id into l_file.id
	  log errors into files_err reject limit 0;

    return l_file;

  end;


  procedure upd_file
    (p_file     in files%rowtype) is

    l_prc_name varchar2(255) := 'upd_file';

  begin

    update files
       set job_name           = p_file.job_name
          ,filename           = p_file.filename
          ,filetype           = p_file.filetype
          ,status_code        = p_file.status_code
          ,records_total      = nvl(p_file.records_total,0)
          ,records_ok         = nvl(p_file.records_ok,0)
          ,records_error      = nvl(p_file.records_error,0)
          ,records_ignored    = nvl(p_file.records_ignored,0)
          ,external_id        = p_file.external_id
     where id = p_file.id
	 log errors into files_err reject limit 0;

  end;


  function register_file
    (p_file     in files%rowtype) return files%rowtype is

    pragma autonomous_transaction;
    l_prc_name varchar2(255) := 'register_file';
    l_id       number(12);
    l_file     files%rowtype:=p_file;


  begin

    if l_file.id is null then
      l_file:=ins_file
        (p_file     => l_file);
    else
      upd_file
        (p_file     => l_file);
    end if;
    commit;
    logger.info(p_file.job_name, M_PACKAGE_NAME, l_prc_name, 'registered file '|| p_file.filename);
    return l_file;

  exception
    when others then
      logger.warn(p_file.job_name, M_PACKAGE_NAME, l_prc_name, 'could not register file '|| p_file.filename);
      return l_file;
  end;


  function get_file_details
    (p_filename  in varchar2) return files%rowtype is

    cursor c_file(b_filename varchar2) is
      select *
      from   files
      where  filename = b_filename;

    r_file  c_file%rowtype;

  begin
    open  c_file(p_filename);
    fetch c_file into r_file;
    close c_file;
    return r_file;
  end get_file_details;



  function get_file_details
    (p_id  in number) return files%rowtype is

    cursor c_file(b_id varchar2) is
      select *
      from   files
      where  id = b_id;

    r_file  c_file%rowtype;

  begin
    open  c_file(p_id);
    fetch c_file into r_file;
    close c_file;
    return r_file;
  end get_file_details;


end register;
/

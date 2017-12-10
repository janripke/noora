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
    l_file     files%rowtype := p_file;

  begin
    --kennen we nog niet het id, dan kan het bestand op basis van
    --job_name nog wel bekend zijn (import aansturing van buiten de applicatie)
    if l_file.id is null
    then
      l_file.id := get_file_id(p_job_name => p_file.job_name);
    end if;
	  if l_file.id is not null then
	    upd_file
          (p_file     => l_file);
	  else
	    l_file := ins_file
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
  

  function get_file_details
    (p_filename    in varchar2
    ,p_status_code in varchar2) return files%rowtype is

    cursor c_file(b_filename varchar2,b_status_code varchar2) is
      select *
      from   files
      where  filename = b_filename
      and    status_code = b_status_code;

    r_file  c_file%rowtype;

  begin
    open  c_file(p_filename,p_status_code);
    fetch c_file into r_file;
    close c_file;
    return r_file;
  end get_file_details;

  
  procedure file_imported_before
    (p_filename in varchar2) is

    l_count            number(12);
    l_file             files%rowtype;

  begin
    l_file := get_file_details(p_filename => p_filename, p_status_code=> register.G_STATUS_IMPORTED);
    if l_file.id is not null then
      raise_application_error(-20107,register.G_FILE_IMPORTED_BEFORE);
    end if;

  end;

  function get_file_id
    (p_job_name  in varchar2) return number is

    cursor c_file(b_job_name varchar2) is
      select *
      from   files
      where  job_name = b_job_name;

    r_file  c_file%rowtype;
  begin
    open  c_file(p_job_name);
    fetch c_file into r_file;
    close c_file;
    return r_file.id;
  end get_file_id;

end register;
/

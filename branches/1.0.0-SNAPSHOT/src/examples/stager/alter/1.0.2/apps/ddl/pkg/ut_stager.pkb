create or replace package body ut_stager as

  M_PACKAGE_NAME           constant varchar2(50) := lower($$plsql_unit);
  M_JOB_PREFIX             constant varchar2(255):= 'UT_STAGER';
  M_OPEN_MODE              constant varchar2(1)  :='W';
  M_FOLDER                 constant varchar2(255):='STAGER_IMPORT';
  M_FILENAME_PREFIX        constant varchar2(50) :='STAGE';
  M_FILENAME_EXT           constant varchar2(50) :='.dat';

  M_FILE_HEADER            constant varchar2(50):='ut_stager.file_header';


  procedure write_header
    (p_handle      in utl_file.file_type
    ,p_file_header in varchar2) is
  begin
    utl_file.put_line(p_handle, p_file_header);
  end;


  procedure write_record
    (p_handle                 in utl_file.file_type
    ,p_line                   in varchar2) is
  begin
    utl_file.put_line(p_handle, p_line);
  end;



  procedure create_test_file
    (p_job_name      in varchar2
    ,p_folder        in varchar2
    ,p_filename      in varchar2
    ,p_header        in varchar2
    ,p_lines         in app_utl.t_collection) is

    l_handle  utl_file.file_type;
    l_prc_name varchar2(255):='create_test_file';

  begin

    l_handle:=app_utl.open_file
      (p_folder    => p_folder
      ,p_filename  => p_filename
      ,p_open_mode => M_OPEN_MODE);

    write_header
      (p_handle      => l_handle
      ,p_file_header => p_header);

    if p_lines.count>0 then
      for i in p_lines.first..p_lines.last loop
        write_record
          (p_handle => l_handle
          ,p_line   => p_lines(i));
      end loop;
	end if;

    app_utl.close_file
      (p_handle   => l_handle
      ,p_filename => p_filename);

  end create_test_file;



  function get_unique_filename
    (p_job_name in varchar2) return varchar2 is

    l_timestamp  varchar2(255):=to_char(sysdate,'yyyymmdd_hh24miss');
    l_filename   varchar2(255);

  begin

    l_filename:=M_FILENAME_PREFIX || '_' ||
                l_timestamp       ||
                M_FILENAME_EXT;

    return l_filename;

  end;



  function create_sample_file(p_job_name in varchar2) return varchar2 is
    l_filename                varchar2(255);
    l_header                  varchar2(4000);
    l_lines                   app_utl.t_collection;

  begin
    l_filename:=get_unique_filename(p_job_name);
    l_header:=app_props.get_property(M_FILE_HEADER);

    l_lines(l_lines.count + 1):= 'mercury|planet';
    l_lines(l_lines.count + 1):= 'venus|planet';
    l_lines(l_lines.count + 1):= 'earth|planet';
    l_lines(l_lines.count + 1):= 'mars|planet';

    create_test_file
      (p_job_name => p_job_name
      ,p_folder   => M_FOLDER
      ,p_filename => l_filename
      ,p_header   => l_header
      ,p_lines    => l_lines);

	return l_filename;

  end;



  -- Deze test slaagt wanneer er 3 rijen met succes zijn opgevoerd.
  procedure t_stager_pass is

    l_job_name                varchar2(255);
    l_filename                varchar2(255);
    l_result                  varchar2(1024);
    l_header                  varchar2(4000);
    l_prc_name                varchar2(255):='[t_import_pass]';
    l_lines                   app_utl.t_collection;
    l_count                   number(12);

  begin
    l_job_name:= app_utl.get_job_name(p_prefix => M_JOB_PREFIX);
    logger.info(l_job_name, M_PACKAGE_NAME, l_prc_name, 'started');
    l_filename:=get_unique_filename(l_job_name);
    l_header:=app_props.get_property(M_FILE_HEADER);

    l_lines(l_lines.count + 1):= 'mercury|planet';
    l_lines(l_lines.count + 1):= 'venus|planet';
    l_lines(l_lines.count + 1):= 'earth|planet';
    l_lines(l_lines.count + 1):= 'mars|planet';

    create_test_file
      (p_job_name => l_job_name
      ,p_folder   => M_FOLDER
      ,p_filename => l_filename
      ,p_header   => l_header
      ,p_lines    => l_lines);

    rpm_imp_siebeldump.start_import
      (p_job_name  => l_job_name
      ,p_filename  => l_filename
      ,p_test_mode => RPM_GENERAL.G_YES);

    rollback;
    logger.info(l_job_name, M_PACKAGE_NAME, l_prc_name, 'finished');

  end t_import_pass;

end ut_stager;
/

create or replace package body iconverter as

  M_PACKAGE_NAME     constant varchar2(256):=upper($$plsql_unit);
  
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

  procedure convert
    (url                in varchar2
    ,sourceCharset      in varchar2
    ,targetCharset      in varchar2) AS 
    LANGUAGE JAVA NAME 
      'com.twoorganize.kpn.IConv.convert
      (java.lang.String
      ,java.lang.String
      ,java.lang.String)';


  procedure convert
    (p_job_name       in varchar2
    ,p_folder         in varchar2
    ,p_filename       in varchar2
    ,p_source_charset in varchar2
    ,p_target_charset in varchar2) is

    l_os_sep             varchar2(10);
    l_url                varchar2(1024);
    l_folder             varchar2(1024);
    l_prc_name           varchar2(255):='convert';

  begin
    l_os_sep := app_props.get_property('OS.SEP');
    l_folder := get_directory_details(p_folder).directory_path;
    l_url := l_folder || l_os_sep || p_filename;
    logger.info(p_job_name,M_PACKAGE_NAME,l_prc_name,'converting file : ' || l_url);
    convert
      (url  => l_url
      ,sourceCharset => p_source_charset
      ,targetCharset => p_target_charset);      
  end;




    

  end iconverter;
/ 

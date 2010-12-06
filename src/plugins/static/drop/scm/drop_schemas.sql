declare
  cursor c_user_xml_schemas is
    select schema_url
    from user_xml_schemas;
  M_QUOTE       varchar2(1):=chr(39);
  statement	varchar2(1024);
  schema_url    varchar2(256);
  constraint_name varchar2(256);

begin
  for user_xml_schema in c_user_xml_schemas loop
    schema_url:=user_xml_schema.schema_url;

    statement:='BEGIN DBMS_XMLSCHEMA.DELETESCHEMA( ' || M_QUOTE || schema_url || M_QUOTE || ',DBMS_XMLSCHEMA.delete_cascade_force); END;';
    dbms_output.put_line(statement);
    execute immediate statement;
  end loop;
end;
/

create table LOG (
  ID                      number(12) not null,
  LOGTYPE_CODE            varchar2(50),
  JOB_NAME                varchar2(255),
  PACKAGE_NAME            varchar2(255),
  METHOD_NAME             varchar2(255),
  MESSAGE                 varchar2(4000),
  UNIQ_SESSION_ID         varchar2(255),
  FORMAT_ERROR_BACKTRACE  varchar2(4000),
  FORMAT_ERROR_STACK      varchar2(4000),
  FORMAT_CALL_STACK       varchar2(4000),  
  CREATED_AT              date,
  CREATED_BY              varchar2(45),
  UPDATED_AT              date,
  UPDATED_BY              varchar2(45)  
);

alter table LOG add constraint LOG_ID_PK primary key (ID) using index;
alter table LOG add constraint LOG_LOGTYPE_CODE_NN check (logtype_code is not null);
alter table LOG add constraint LOG_LOGTYPE_CODE_IN check (logtype_code in('TRACE','DEBUG','INFO','WARN','ERROR','FATAL'));
alter table LOG add constraint LOG_MESSAGE_NN check (message is not null);
alter table LOG add constraint LOG_UNIQ_SESSION_ID_NN check (uniq_session_id is not null);
alter table LOG add constraint LOG_CREATED_AT_NN check (created_at is not null);
alter table LOG add constraint LOG_CREATED_BY_NN check (created_by is not null);
alter table LOG add constraint LOG_UPDATED_AT_NN check (updated_at is not null);
alter table LOG add constraint LOG_UPDATED_BY_NN check (created_by is not null);

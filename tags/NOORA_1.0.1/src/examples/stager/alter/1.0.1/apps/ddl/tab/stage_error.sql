create table stage_error
(id                           number(12) not null
,key_id                       number(12)
,job_name                     varchar2(255 char)
,table_name                   varchar2(255 char)
,error_table_name             varchar2(255 char)
,column_name                  varchar2(255 char)
,ora_err_number               number(12)
,ora_err_mesg                 varchar2(2000 byte)
,created_at                   date
,created_by                   varchar2(45 char)
,updated_at                   date
,updated_by                   varchar2(45 char)
) nologging;


alter table stage_error add constraint SE_ID_PK primary key (ID) using index nologging;
                                                                                                 
-- Create/Recreate check constraints                                                             
alter table stage_error add constraint SE_KEY_ID_NN  check (key_id is not null);
alter table stage_error add constraint SE_JOB_NAME_NN  check (job_name is not null);
alter table stage_error add constraint SE_TABLE_NAME_NN  check (table_name is not null);
alter table stage_error add constraint SE_ERROR_TABLE_NAME_NN  check (error_table_name is not null);
alter table stage_error add constraint SE_COLUMN_NAME_NN  check (column_name is not null);
alter table stage_error add constraint SE_ORA_ERR_NUMBER_NN  check (ora_err_number is not null);
alter table stage_error add constraint SE_ORA_ERR_MESG_NN  check (ora_err_mesg is not null);

alter table stage_error add constraint SE_CREATED_AT_NN  check (created_at is not null);
alter table stage_error add constraint SE_CREATED_BY_NN  check (created_by is not null);  
alter table stage_error add constraint SE_UPDATED_AT_NN  check (updated_at is not null);
alter table stage_error add constraint SE_UPDATED_BY_NN  check (updated_by is not null);


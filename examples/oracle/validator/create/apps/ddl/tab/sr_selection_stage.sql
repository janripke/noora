create table sr_selection_stage
(id                                     number(12) not null
,line_id                                number(12)
,job_name                               varchar2(255)
,created_at                             date
,created_by                             varchar2(45)
,updated_at                             date
,updated_by                             varchar2(45)
,account_number							varchar2(4000)
,active                                 varchar2(4000)
) nologging;                                                                                       

alter table sr_selection_stage add constraint sr_ss_ID_PK primary key (ID) using index nologging;
                                                                                                 
-- Create/Recreate check constraints                                                             
   
alter table sr_selection_stage add constraint sr_ss_line_id_nn check (line_id is not null);
alter table sr_selection_stage add constraint sr_ss_created_at_nn check (created_at is not null);
alter table sr_selection_stage add constraint sr_ss_created_by_nn check (created_by is not null);
alter table sr_selection_stage add constraint sr_ss_job_name_nn   check (job_name is not null);  
alter table sr_selection_stage add constraint sr_ss_updated_at_nn check (updated_at is not null);
alter table sr_selection_stage add constraint sr_ss_updated_by_nn check (updated_by is not null);
create table sr_selection
(id                           number(12) not null
,stage_id                     number(12)
,account_number               number(10)
,active	                      number(1) default 1  
,value                        varchar2(256)
,created_at                   date
,created_by                   varchar2(45)
,updated_at                   date
,updated_by                   varchar2(45)
) nologging;


alter table sr_selection add constraint SR_SN_ID_PK primary key (ID) using index nologging;
                                                                                                 
-- Create/Recreate check constraints                                                             
alter table sr_selection add constraint SR_SN_CREATED_AT_NN  check (created_at is not null);
alter table sr_selection add constraint SR_SN_CREATED_BY_NN  check (created_by is not null);  
alter table sr_selection add constraint SR_SN_UPDATED_AT_NN  check (updated_at is not null);
alter table sr_selection add constraint SR_SN_UPDATED_BY_NN  check (updated_by is not null);
alter table sr_selection add constraint SR_SN_STAGE_ID_NN check (stage_id is not null);


alter table sr_selection add constraint SR_SN_ACCOUNT_NUMBER_NN check (account_number is not null);
alter table sr_selection add constraint SR_SN_ACTIVE_NN check (active is not null);

alter table sr_selection add constraint SR_SN_ACTIVE_IN check (active in (0,1));

alter table sr_selection add constraint SR_SN_ACCOUNT_NUMBER_UNIQ unique (account_number) using index nologging tablespace ts_index;

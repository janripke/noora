create table sr_mapping
(id                           number(12) not null
,name                         varchar2(50)
,value                        varchar2(256)
,created_at                   date
,created_by                   varchar2(45)
,updated_at                   date
,updated_by                   varchar2(45)
) nologging;


alter table sr_mapping add constraint sr_mg_id_pk primary key (ID) using index nologging;
                                                                                                 
-- Create/Recreate check constraints                                                             
alter table sr_mapping add constraint sr_mg_name_nn  check (name is not null);
alter table sr_mapping add constraint sr_mg_value_nn check (value is not null);
alter table sr_mapping add constraint sr_mg_created_at_nn  check (created_at is not null);
alter table sr_mapping add constraint sr_mg_created_by_nn  check (created_by is not null);  
alter table sr_mapping add constraint sr_mg_updated_at_nn  check (updated_at is not null);
alter table sr_mapping add constraint sr_mg_updated_by_nn  check (updated_by is not null);


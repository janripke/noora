create table APPLICATION_PROPERTIES
(
  ID                      NUMBER(12) not null,
  NAME                    VARCHAR2(255),
  VALUE                   VARCHAR2(4000),
  DESCRIPTION             VARCHAR2(255),
  CREATED_AT              date,
  CREATED_BY              varchar2(45),
  UPDATED_AT              date,
  UPDATED_BY              varchar2(45)
);


alter table APPLICATION_PROPERTIES add constraint APP_PROP_ID_PK primary key (ID) using index;
alter table APPLICATION_PROPERTIES add constraint APP_PROP_NAME_NN check (name is not null);
alter table APPLICATION_PROPERTIES add constraint APP_PROP_VALUE_NN check (value is not null);
alter table APPLICATION_PROPERTIES add constraint APP_PROP_CREATED_AT_NN check (created_at is not null);
alter table APPLICATION_PROPERTIES add constraint APP_PROP_CREATED_BY_NN check (created_by is not null);
alter table APPLICATION_PROPERTIES add constraint APP_PROP_UPDATED_AT_NN check (updated_at is not null);
alter table APPLICATION_PROPERTIES add constraint APP_PROP_UPDATED_BY_NN check (updated_by is not null);

alter table APPLICATION_PROPERTIES add constraint APP_PROP_NAME_UNIQ unique (NAME) using index;

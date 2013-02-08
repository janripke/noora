CREATE TABLE application_properties
(
  id 				   INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name 				 VARCHAR(100) NOT NULL,
  value        VARCHAR(4000) NOT NULL,
  description  VARCHAR(255),
  created_at   DATETIME NOT NULL,
  created_by   VARCHAR(45) NOT NULL,
  updated_at   DATETIME NOT NULL,
  updated_by   VARCHAR(45) NOT NULL
);


# alter table APPLICATION_PROPERTIES add constraint APP_PROP_ID_PK primary key (ID) using index;
# alter table APPLICATION_PROPERTIES add constraint APP_PROP_NAME_NN check (name is not null);
# alter table APPLICATION_PROPERTIES add constraint APP_PROP_VALUE_NN check (value is not null);
# alter table APPLICATION_PROPERTIES add constraint APP_PROP_CREATED_AT_NN check (created_at is not null);
# alter table APPLICATION_PROPERTIES add constraint APP_PROP_CREATED_BY_NN check (created_by is not null);
# alter table APPLICATION_PROPERTIES add constraint APP_PROP_UPDATED_AT_NN check (updated_at is not null);
# alter table APPLICATION_PROPERTIES add constraint APP_PROP_UPDATED_BY_NN check (updated_by is not null);

ALTER TABLE application_properties ADD CONSTRAINT ap_name_uniq UNIQUE INDEX (name);

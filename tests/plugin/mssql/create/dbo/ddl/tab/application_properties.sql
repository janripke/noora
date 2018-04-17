create table application_properties
(
  id                      bigint primary key not null default (next value for application_properties_s),
  name                    varchar(255),
  value                   varchar(4000),
  description             varchar(255),
  created_at              datetime,
  created_by              varchar(45),
  updated_at              datetime,
  updated_by              varchar(45)
);
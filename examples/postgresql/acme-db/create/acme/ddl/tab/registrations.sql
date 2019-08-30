create table registrations
(
  id            integer primary key not null,
  job_name      varchar(255),
  uuid          varchar(255),
  parent_id     integer,
  location      varchar(255),
  name          varchar(255),
  type          varchar(30),
  kind          varchar(30),
  size          integer default 0,
  state         varchar(50),
  error_code    varchar(50),
  check_point   varchar(40),
  records_total integer default 0,
  records_ok    integer default 0,
  records_error integer default 0,
  active        integer default 1,
  created_at    timestamp not null,
  created_by    varchar(45) not null,
  updated_at    timestamp not null,
  updated_by    varchar(45) not null
);
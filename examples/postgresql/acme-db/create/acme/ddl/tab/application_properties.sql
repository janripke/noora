CREATE TABLE application_properties
(
  id INTEGER PRIMARY KEY DEFAULT NEXTVAL('application_properties_s')
, name VARCHAR(100) not null unique
, value VARCHAR(4000) not null
, description VARCHAR(255)
, created_at VARCHAR NOT NULL
, created_by VARCHAR(45) NOT NULL
, updated_at TIMESTAMP NOT NULL
, updated_by VARCHAR(45) NOT NULL
);
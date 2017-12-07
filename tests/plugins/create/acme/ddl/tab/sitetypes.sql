CREATE TABLE sitetypes 
(
  id                  int(11) NOT NULL AUTO_INCREMENT primary key,
  sitetype            varchar(255) NOT NULL unique,
  created_at          datetime NOT NULL,
  created_by          varchar(45) NOT NULL,
  updated_at          datetime NOT NULL,
  updated_by          varchar(45) NOT NULL
);





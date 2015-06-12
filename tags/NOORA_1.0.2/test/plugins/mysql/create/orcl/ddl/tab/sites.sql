CREATE TABLE sites 
(
  id                  int(11) NOT NULL AUTO_INCREMENT primary key,
  name                varchar(255) NOT NULL unique,
  url                 varchar(255) NOT NULL unique,
  hashcode            varchar(255) NOT NULL,
  description         varchar(4000) DEFAULT NULL,
  delay               int(11) DEFAULT NULL,
  delay_unit          varchar(45) DEFAULT NULL,
  delay_in_seconds    int(11) DEFAULT '0',
  paylimit            varchar(255) DEFAULT NULL,
  paylimit_currency   varchar(45) DEFAULT NULL,
  earnings_per_visit  int(11) DEFAULT '0',
  created_at          datetime NOT NULL,
  created_by          varchar(45) NOT NULL,
  updated_at          datetime NOT NULL,
  updated_by          varchar(45) NOT NULL
);





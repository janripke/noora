CREATE TABLE delay_units 
(
  id          int(11) NOT NULL AUTO_INCREMENT primary key,
  delay_unit  varchar(255) NOT NULL UNIQUE,
  created_at  datetime NOT NULL,
  created_by  varchar(45) NOT NULL,
  updated_at  datetime NOT NULL,
  updated_by  varchar(45) NOT NULL
);




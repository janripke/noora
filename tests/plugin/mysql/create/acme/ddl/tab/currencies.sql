CREATE TABLE currencies 
(
  id            int(11) NOT NULL AUTO_INCREMENT primary key,
  currency      varchar(255) NOT NULL,
  created_at    datetime NOT NULL,
  created_by    varchar(45) NOT NULL,
  updated_at    datetime NOT NULL,
  updated_by    varchar(45) NOT NULL
);



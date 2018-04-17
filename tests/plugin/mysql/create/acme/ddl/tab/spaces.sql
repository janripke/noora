CREATE TABLE spaces
(
  id          int(11) NOT NULL AUTO_INCREMENT primary key,
  hashcode    varchar(255) NOT NULL,
  title       text,
  created_at  datetime NOT NULL,
  created_by  varchar(45) NOT NULL,
  updated_at  datetime NOT NULL,
  updated_by  varchar(45) NOT NULL
);


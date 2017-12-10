CREATE TABLE levels
(
  id          int(11) NOT NULL AUTO_INCREMENT primary key,
  level       int(11) NOT NULL,
  points      int(11) default 0,
  created_at  datetime NOT NULL,
  created_by  varchar(45) NOT NULL,
  updated_at  datetime NOT NULL,
  updated_by  varchar(45) NOT NULL
);


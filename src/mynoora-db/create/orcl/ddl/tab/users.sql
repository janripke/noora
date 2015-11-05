CREATE TABLE  users 
(
  id               int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  grp_id           int(11) NOT NULL,
  hashcode         varchar(255) NOT NULL,
  username         varchar(255) NOT NULL unique KEY,
  password         varchar(255) DEFAULT NULL,
  email            varchar(255) DEFAULT NULL unique KEY,
  created_at       datetime NOT NULL,
  created_by       varchar(45) NOT NULL,
  updated_at       datetime NOT NULL,
  updated_by       varchar(45) NOT NULL
);







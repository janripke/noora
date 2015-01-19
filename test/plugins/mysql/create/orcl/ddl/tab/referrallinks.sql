CREATE TABLE referrallinks
(
  id           int(11) NOT NULL AUTO_INCREMENT primary key,
  url          varchar(255) NOT NULL,
  hashcode     varchar(255) NOT NULL,
  usr_id       int(11) NOT NULL,
  ste_id       int(11) DEFAULT NULL,
  username     varchar(255) DEFAULT NULL,
  password     varchar(255) DEFAULT NULL,
  on_hold_ind  int(11) DEFAULT '0',
  address      varchar(255) DEFAULT NULL,
  created_at   datetime NOT NULL,
  created_by   varchar(45) NOT NULL,
  updated_at   datetime NOT NULL,
  updated_by   varchar(45) NOT NULL
);






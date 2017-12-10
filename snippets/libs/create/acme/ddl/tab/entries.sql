CREATE TABLE entries 
(
  id          int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  title       text,
  content     text,
  spe_id      int(11) DEFAULT NULL,
  hashcode    varchar(255) NOT NULL,
  posted_on   datetime DEFAULT NULL,
  created_at  datetime NOT NULL,
  created_by  varchar(45) NOT NULL,
  updated_at  datetime NOT NULL,
  updated_by  varchar(45) NOT NULL 
);




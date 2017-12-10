CREATE TABLE comments
(
  id           int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  eny_id       int(11) DEFAULT NULL,
  hashcode     varchar(255) NOT NULL,
  content      text,
  posted_on    datetime DEFAULT NULL,
  created_at   datetime NOT NULL,
  created_by   varchar(45) NOT NULL,
  updated_at   datetime NOT NULL,
  updated_by   varchar(45) NOT NULL
);

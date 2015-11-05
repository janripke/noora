CREATE TABLE projectfiles
(
  id          int(11) NOT NULL AUTO_INCREMENT primary key,
  hashcode    varchar(255) NOT NULL,
  filename    varchar(50) NOT NULL,
  pjt_id      int(11) NOT NULL,
  created_at  datetime NOT NULL,
  created_by  varchar(45) NOT NULL,
  updated_at  datetime NOT NULL,
  updated_by  varchar(45) NOT NULL
);




CREATE TABLE sessions
(
  session_id  char(128) NOT NULL UNIQUE,
  atime       timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  data        text
);

CREATE TABLE log (
  id                      INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  logtype_code            VARCHAR(50) NOT NULL,
  job_name                VARCHAR(255),
  package_name            VARCHAR(255),
  method_name             VARCHAR(255),
  message                 VARCHAR(4000) NOT NULL,
  unique_session_id         VARCHAR(255),
  format_error_backtrace  VARCHAR(4000),
  format_error_stack      VARCHAR(4000),
  format_call_stack       VARCHAR(4000),  
  created_at              DATETIME NOT NULL,
  created_by              VARCHAR(45) NOT NULL,
  updated_at              DATETIME NOT NULL,
  updated_by              VARCHAR(45) NOT NULL  
);



create global temporary table STAGE_RESULT
(
  ID                      NUMBER(12),
  TYPE                    VARCHAR2(255),
  JOB_NAME                VARCHAR2(255),
  INFO                    VARCHAR2(4000),
  CONTENT                 CLOB
)
on commit delete rows;

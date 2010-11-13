create index FI_FILENAME_IDX on FILES (FILENAME) nologging;
create index FI_FK_STATUS_CODE_IDX on FILES (STATUS_CODE) nologging;
create index FI_FK_FILETYPE_CODE_IDX on FILES (FILETYPE) nologging;
create index FI_MK_FILENAME_IDX on FILES (FILENAME,STATUS_CODE) nologging;
create index FI_JOB_NAME_CODE_IDX on FILES (JOB_NAME) nologging;

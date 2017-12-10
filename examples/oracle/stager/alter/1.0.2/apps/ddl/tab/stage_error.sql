alter table STAGE_ERROR add line_id number(12);
alter table STAGE_ERROR drop constraint SE_KEY_ID_NN;
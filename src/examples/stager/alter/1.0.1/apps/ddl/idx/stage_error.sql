create index e_key_id_idx on stage_error (key_id) nologging;
create index e_job_name_idx on stage_error (job_name) nologging;
create index e_sk1_idx on stage_error (job_name,key_id) nologging;

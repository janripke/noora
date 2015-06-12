alter table sr_selection add constraint sr_sn_stage_id_fk foreign key (stage_id)
references sr_selection_stage (id);


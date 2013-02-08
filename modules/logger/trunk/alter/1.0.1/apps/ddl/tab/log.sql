alter table LOG drop constraint LOG_UPDATED_BY_NN;
alter table LOG add constraint LOG_UPDATED_BY_NN check (updated_by is not null);

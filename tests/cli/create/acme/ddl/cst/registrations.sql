alter table registrations add constraint rgn_parent_id foreign key (parent_id) references registrations (id);

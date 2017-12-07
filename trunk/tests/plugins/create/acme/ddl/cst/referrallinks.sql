ALTER TABLE referrallinks ADD CONSTRAINT rlk_ste_id_fk FOREIGN KEY (ste_id) REFERENCES sites (id);
ALTER TABLE referrallinks ADD CONSTRAINT rlk_usr_id_fk FOREIGN KEY (usr_id) REFERENCES users (id);
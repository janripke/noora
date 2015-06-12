ALTER TABLE users ADD CONSTRAINT usr_grp_id_fk FOREIGN KEY (grp_id) REFERENCES groups (id);
ALTER TABLE users ADD CONSTRAINT usr_referral_id_fk FOREIGN KEY (referral_id) REFERENCES users (id);
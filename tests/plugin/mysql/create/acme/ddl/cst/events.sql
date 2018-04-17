ALTER TABLE events ADD CONSTRAINT evt_rlk_id_fk FOREIGN KEY (rlk_id) REFERENCES referrallinks (id);

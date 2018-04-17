ALTER TABLE comments ADD CONSTRAINT cmt_eny_fk FOREIGN KEY (eny_id) REFERENCES entries (id);

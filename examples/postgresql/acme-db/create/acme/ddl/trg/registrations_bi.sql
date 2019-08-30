create trigger registrations_bi
    before insert
    on registrations
    for each row
execute procedure registrations_bi();
create trigger registrations_bu
    before update
    on registrations
    for each row
execute procedure registrations_bu();
create or replace trigger holidays_biu
  before insert or update on holidays
  for each row

declare
begin
  if inserting then
    if :new.id is null then
      select holidays_s.nextval
      into   :new.id
      from   dual;
    end if;
    :new.created_at:=sysdate;
    :new.created_by:=user;
  end if;
  :new.updated_at:=sysdate;
  :new.updated_by:=user;
end;
/

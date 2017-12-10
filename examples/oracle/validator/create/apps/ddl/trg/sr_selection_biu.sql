create or replace trigger sr_selection_biu
  before insert or update on sr_selection
  for each row

declare
  l_sysdate date:=sysdate;
begin
  if inserting then
    if :new.id is null then
      select sr_selection_s.nextval
      into   :new.id
      from   dual;
    end if;
    :new.created_at:=l_sysdate;
    :new.created_by:=user;
  end if;
  :new.updated_at:=l_sysdate;
  :new.updated_by:=user;
end;
/
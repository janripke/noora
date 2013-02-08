create or replace trigger stage_error_biu
  before insert or update on stage_error
  for each row

declare
  l_sysdate date:=sysdate;
begin
  if inserting then
    if :new.id is null then
      select stage_error_s.nextval
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

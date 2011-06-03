create or replace trigger files_biu
  before insert or update on files
  for each row

begin
  if inserting then
    if :new.id is null then
      select files_s.nextval
      into   :new.id
      from   dual;
    end if;
    :new.created_at:=sysdate;
    :new.created_by:=user;
    :new.updated_at:=sysdate;
    :new.updated_by:=user;
  elsif updating then
    :new.updated_at:=sysdate;
    :new.updated_by:=user;
  end if;
end files_biu;
/

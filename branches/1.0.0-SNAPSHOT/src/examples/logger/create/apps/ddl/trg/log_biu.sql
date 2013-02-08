create or replace trigger log_biu
  before insert or update on log
  for each row
begin
  if inserting then
    if :new.id is null then
      select log_s.nextval 
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
end log_biu;
/

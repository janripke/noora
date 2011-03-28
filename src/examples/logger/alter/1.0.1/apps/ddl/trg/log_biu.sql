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
    if :new.created_by is null then
      :new.created_by:=user;
    end if;
    if :new.updated_by is null then
      :new.updated_by:=user;
    end if;    
    :new.created_at:=sysdate;
    :new.updated_at:=sysdate;   
  elsif updating then
    :new.updated_at:=sysdate;
    if :new.updated_by is null then
      :new.updated_by:=user;
    end if;
  end if;
end log_biu;
/

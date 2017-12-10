create or replace trigger application_properties_biu
  before insert or update on application_properties
  for each row
begin
  if inserting then
    if :new.id is null then
      select application_properties_s.nextval 
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
end application_properties_biu;
/

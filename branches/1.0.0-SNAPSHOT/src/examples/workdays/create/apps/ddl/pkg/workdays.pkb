create or replace package body workdays as
  
  function add_workdays
    (p_date in date, p_days in number) return date is
 
    l_date         date  := p_date;
    l_day_of_week  number;
    i              number:=0;
    l_count        number:=0;
    l_sign         number:=sign(p_days);
    l_saturday     varchar2(1):=to_char(to_date('06-11-2010','DD-MM-YYYY'),'D');
    l_sunday       varchar2(1):=to_char(to_date('07-11-2010','DD-MM-YYYY'),'D');
 
  begin
    
    while l_count < abs(p_days) loop
      l_date:=l_date+l_sign;
      l_day_of_week:=to_char(l_date,'D');
      if l_day_of_week not in (l_sunday,l_saturday) and not is_holiday(l_date) then
        l_count:=l_count+1;
      end if;

    end loop;
    return l_date;
    
  end;

  function is_holiday
    (p_date in date) return boolean is

    l_count number(12);
    l_result boolean := false;
    l_year   number(4) := to_char(p_date,'yyyy');

  begin
    select count(0)
    into   l_count
    from   holidays
    where  day = trunc(p_date)
    and    year = l_year;

    if l_count <> 0 then
      l_result := true;
    end if;

    return l_result;
  end;

end workdays;
/

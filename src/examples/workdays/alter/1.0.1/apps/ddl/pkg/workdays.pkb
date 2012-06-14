create or replace package body workdays as

  type t_holidays IS TABLE OF number(1)
    INDEX BY VARCHAR2(8);

  gt_holidays t_holidays;

  cursor c_holiday
  is
    select day
    from   holidays;

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


  function is_workday(p_date in date) return boolean is
    l_day_of_week  number;
    l_saturday     varchar2(1):=to_char(to_date('06-11-2010','DD-MM-YYYY'),'D');
    l_sunday       varchar2(1):=to_char(to_date('07-11-2010','DD-MM-YYYY'),'D');
  begin
      l_day_of_week:=to_char(p_date,'D');
      if l_day_of_week not in (l_sunday,l_saturday) and not is_holiday(p_date) then
        return true;
      end if;
    return false;
  end;


  function is_holiday
    (p_date in date) return boolean is

    l_count number(12);
    l_result boolean := false;

  begin
    if gt_holidays.exists(to_char(p_date,'yyyymmdd'))
    then
      l_result :=  true;
    end if;

    return l_result;
  end;
  --
  --DJN
  --Tijdens de 1ste aanroep van deze package wordt de collection gevuld met alle feestdagen.
  --De index wordt "misbruikt" zodat we in de is_holiday een exists kunnen gebruiken.
  --
  --Omdat we nu alle feestdagen in een collection hebben staan kunen we snel de feestdagen
  --opzoeken zonder dat er iedere keer een query uitgevoerd moet worden.
  begin
    for r_holiday in c_holiday
    loop
       gt_holidays(to_char(r_holiday.day,'yyyymmdd')) := 1;
     end loop;
end workdays;
/

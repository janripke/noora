create view referrallinks_v as 
select rlk.id           as id,
       rlk.url          as url,
       rlk.hashcode     as hashcode,
       rlk.usr_id       as usr_id,
       rlk.username     as username,
       rlk.password     as password,
       rlk.on_hold_ind  as on_hold_ind,
       rlk.dead_ind     as dead_ind,
       rlk.amount       as amount,
       rlk.address      as address,
       mwt.name         as microwallet,
       mwt.microwallet_parameters as microwallet_parameters,
       rlk.created_at   as created_at,
       rlk.created_by   as created_by,
       rlk.updated_at   as updated_at,
       rlk.updated_by   as updated_by,
       ste.name         as name,
       ste.delay        as delay,
       ste.delay_unit   as delay_unit,
       COUNT(evt.id)    as clicks,
       ste.owner        as owner,
       ste.microwallet  as ste_microwallet,
       format((rlk.amount*100000000)/COUNT(evt.id),0) as faucet_value,
       ifnull(time_to_sec(timediff(now(), max(evt.created_at))),
       ifnull(ste.delay_in_seconds,-(1))) as last_visited_in_seconds,
       ifnull(ste.delay_in_seconds,-(1))  as delay_in_seconds        
from referrallinks rlk 
left join events evt on rlk.id = evt.rlk_id 
left join sites  ste on rlk.ste_id = ste.id 
left join sites  mwt on ste.microwallet = mwt.name
group by rlk.id
        ,rlk.url
        ,rlk.hashcode
        ,rlk.usr_id
        ,rlk.username
        ,rlk.password
        ,rlk.on_hold_ind
        ,rlk.dead_ind
        ,rlk.amount
        ,rlk.address
        ,mwt.microwallet
        ,mwt.microwallet_parameters
        ,rlk.created_at
        ,rlk.created_by
        ,rlk.updated_at
        ,rlk.updated_by
        ,ste.name
        ,ste.delay
        ,ste.delay_unit
        ,ste.delay_in_seconds
        ,ste.microwallet
;

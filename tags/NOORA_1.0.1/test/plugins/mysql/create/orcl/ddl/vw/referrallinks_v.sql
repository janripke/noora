
CREATE VIEW referrallinks_v AS 
select rlk.id  AS id,
       rlk.url AS url,
       rlk.hashcode AS hashcode,
       `rlk`.`usr_id` AS `usr_id`,
       `rlk`.`username` AS `username`,
       `rlk`.`password` AS `password`,
       `rlk`.`on_hold_ind` AS `on_hold_ind`,
       `rlk`.`address` AS `address`,
       `rlk`.`created_at` AS `created_at`,
       `rlk`.`created_by` AS `created_by`,
       `rlk`.`updated_at` AS `updated_at`,
       `rlk`.`updated_by` AS `updated_by`,
       `ste`.`name` AS `name`,
       `ste`.`delay` AS `delay`,
       `ste`.`delay_unit` AS `delay_unit`,
       ifnull(time_to_sec(timediff(now(),
       max(`evt`.`created_at`))),
       ifnull(`ste`.`delay_in_seconds`,-(1))) AS `last_visited_in_seconds`,
       ifnull(`ste`.`delay_in_seconds`,-(1)) AS `delay_in_seconds` from ((`referrallinks` `rlk` left join `events` `evt` on((`rlk`.`id` = `evt`.`rlk_id`))) left join `sites` `ste` on((`rlk`.`ste_id` = `ste`.`id`))) group by `rlk`.`id`,`rlk`.`url`,`rlk`.`hashcode`,`rlk`.`usr_id`,`rlk`.`username`,`rlk`.`password`,`rlk`.`on_hold_ind`,`rlk`.`address`,`rlk`.`created_at`,`rlk`.`created_by`,`rlk`.`updated_at`,`rlk`.`updated_by`,`ste`.`name`,`ste`.`delay`,`ste`.`delay_unit`,`ste`.`delay_in_seconds`;
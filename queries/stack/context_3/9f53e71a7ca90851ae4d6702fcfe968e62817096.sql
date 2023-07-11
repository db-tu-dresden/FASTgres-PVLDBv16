SELECT acc.location, count(*)
FROM
site as s,
so_user as u1,
question as q1,
answer as a1,
tag as t1,
tag_question as tq1,
badge as b,
account as acc
WHERE
s.site_id = q1.site_id
AND s.site_id = u1.site_id
AND s.site_id = a1.site_id
AND s.site_id = t1.site_id
AND s.site_id = tq1.site_id
AND s.site_id = b.site_id
AND q1.id = tq1.question_id
AND q1.id = a1.question_id
AND a1.owner_user_id = u1.id
AND t1.id = tq1.tag_id
AND b.user_id = u1.id
AND acc.id = u1.account_id
AND (s.site_name in ('es','gis'))
AND (t1.name in ('arcgis-pro','css3','distance','editing','excel','google-earth-engine','layers','mysqli','qgis-processing','query','remote-sensing','symbology','visual-studio','wms'))
AND (q1.view_count >= 10)
AND (q1.view_count <= 1000)
AND (u1.downvotes >= 0)
AND (u1.downvotes <= 10)
AND (b.name in ('Autobiographer','Curious','Notable Question','Popular Question','Revival','Scholar','Student','Supporter','Yearling'))
GROUP BY acc.location
ORDER BY COUNT(*)
DESC
LIMIT 100

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
AND (s.site_name in ('english','gis','math','stats'))
AND (t1.name in ('abstract-algebra','arcgis-10.1','arcgis-10.3','arcgis-javascript-api','arcgis-server','arithmetic','coordinate-system','dynamical-systems','meaning','measure-theory','openlayers','ordinary-differential-equations','postgresql','synonyms'))
AND (q1.score >= 0)
AND (q1.score <= 5)
AND (u1.upvotes >= 10)
AND (u1.upvotes <= 1000000)
AND (b.name in ('Autobiographer','Constituent','Custodian','Editor','Enlightened','Excavator','Explainer','Famous Question','Informed','Nice Question','Popular Question','Promoter','Revival','Student'))
GROUP BY acc.location
ORDER BY COUNT(*)
DESC
LIMIT 100

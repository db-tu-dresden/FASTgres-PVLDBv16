SELECT COUNT(*)
FROM
tag as t,
site as s,
question as q,
tag_question as tq
WHERE
t.site_id = s.site_id
AND q.site_id = s.site_id
AND tq.site_id = s.site_id
AND tq.question_id = q.id
AND tq.tag_id = t.id
AND (s.site_name in ('dba'))
AND (t.name in ('join','mongodb','mysql-5.5','optimization','oracle-11g-r2','sql-server-2005','ssms','stored-procedures'))
AND (q.score >= 0)
AND (q.score <= 1000)

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
AND (s.site_name in ('pt'))
AND (t.name in ('array','asp.net-mvc','banco-de-dados','c','jquery','json','php','sql-server'))
AND (q.view_count >= 10)
AND (q.view_count <= 1000)

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
AND (t.name in ('ajax','array','asp.net-mvc','banco-de-dados','c','html5','laravel'))
AND (q.view_count >= 0)
AND (q.view_count <= 100)

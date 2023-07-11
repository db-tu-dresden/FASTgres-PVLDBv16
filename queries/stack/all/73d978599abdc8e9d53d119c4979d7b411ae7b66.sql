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
AND (s.site_name in ('gamedev'))
AND (t.name in ('2d','android','collision-detection','physics'))
AND (q.view_count >= 10)
AND (q.view_count <= 1000)

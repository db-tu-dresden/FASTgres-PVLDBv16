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
AND (s.site_name in ('stackoverflow'))
AND (t.name in ('asp.net-mvc-5','attributes','com','console','foreach','glsl','multithreading','operating-system','outlook','pdo','scipy','ssl','zend-framework'))
AND (q.favorite_count >= 0)
AND (q.favorite_count <= 10000)

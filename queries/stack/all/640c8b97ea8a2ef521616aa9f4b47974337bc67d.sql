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
AND (t.name in ('api','asp.net-mvc-3','asynchronous','authentication','collections','events','excel','exception','file-io','go','image-processing','intellij-idea','optimization','sql-server-2008','vb.net'))
AND (q.favorite_count >= 5)
AND (q.favorite_count <= 5000)

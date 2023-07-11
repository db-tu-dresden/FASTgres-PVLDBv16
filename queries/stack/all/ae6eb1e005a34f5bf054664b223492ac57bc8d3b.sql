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
AND (t.name in ('ant','cursor','google-drive-api','ios4','less','msbuild','rabbitmq','repository','rounding','selenium-chromedriver','sql-server-2005','xpages'))
AND (q.view_count >= 10)
AND (q.view_count <= 1000)

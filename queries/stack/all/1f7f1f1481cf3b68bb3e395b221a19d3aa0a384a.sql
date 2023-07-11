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
AND (t.name in ('asp.net-mvc-3','asynchronous','callback','character-encoding','console','grails','multithreading','nlp','query-optimization','selenium','selenium-webdriver'))
AND (q.view_count >= 0)
AND (q.view_count <= 100)

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
AND (t.name in ('bots','cocoapods','cross-browser','dialogflow','gmail','jsoup','mocking','nosql','nsstring','regex-lookarounds','rubygems','teradata'))
AND (q.view_count >= 0)
AND (q.view_count <= 100)

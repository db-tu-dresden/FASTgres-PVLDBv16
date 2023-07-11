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
AND (t.name in ('cocoa-touch','functional-programming','github','language-agnostic','sql-server','typescript','uitableview'))
AND (q.score >= 10)
AND (q.score <= 1000)

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
AND (t.name in ('arangodb','correlation','cut','facebook-ios-sdk','http-live-streaming','http-status-code-403','jdeveloper','joomla2.5','jtree','kill','lm','vuforia'))
AND (q.score >= 0)
AND (q.score <= 1000)

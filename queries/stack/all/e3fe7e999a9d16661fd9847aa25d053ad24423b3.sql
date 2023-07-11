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
AND (t.name in ('akka-stream','andengine','arangodb','c#-3.0','calculated-columns','cx-freeze','delimiter','explode','gdi','google-colaboratory','jna','karma-runner','perl6','viewport','yesod'))
AND (q.view_count >= 10)
AND (q.view_count <= 1000)

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
AND (t.name in ('access-token','caliburn.micro','heatmap','kinect','laravel-routing','mvp','opengraph','projection','qtp','text-editor','ubuntu-18.04','webpack-2'))
AND (q.score >= 0)
AND (q.score <= 5)

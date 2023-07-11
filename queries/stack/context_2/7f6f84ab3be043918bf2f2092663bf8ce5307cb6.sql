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
AND (s.site_name in ('android'))
AND (t.name in ('4.4-kitkat','5.0-lollipop','adb','root-access','samsung'))
AND (q.score >= 0)
AND (q.score <= 5)

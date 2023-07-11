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
AND (s.site_name in ('magento'))
AND (t.name in ('admin','checkout','magento-1.8','magento2.2','magento2.3'))
AND (q.score >= 0)
AND (q.score <= 0)

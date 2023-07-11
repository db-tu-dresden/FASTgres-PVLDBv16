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
AND (t.name in ('ado.net','css-float','duplicates','focus','html5-canvas','integer','numbers','profiling','pyqt5','subprocess','timestamp','usb','windows-phone'))
AND (q.favorite_count >= 0)
AND (q.favorite_count <= 1)

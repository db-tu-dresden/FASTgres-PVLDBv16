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
AND (t.name in ('.net','clojure','cookies','google-cloud-firestore','google-maps-api-3','hive','modal-dialog','network-programming','stream','xcode'))
AND (q.favorite_count >= 0)
AND (q.favorite_count <= 10000)

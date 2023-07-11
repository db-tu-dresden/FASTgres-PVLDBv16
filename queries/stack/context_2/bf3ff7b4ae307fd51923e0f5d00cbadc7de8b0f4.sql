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
AND (t.name in ('cs50','directx-11','eclipse-cdt','lotus-domino','ngfor','nvidia','partitioning','php-7','procedure','sfml','speech-to-text','turtle-graphics','webhooks'))
AND (q.view_count >= 10)
AND (q.view_count <= 1000)

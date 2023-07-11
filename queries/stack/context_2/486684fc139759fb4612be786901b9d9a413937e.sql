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
AND (s.site_name in ('superuser'))
AND (t.name in ('cpu','filesystems','hard-drive','macos','microsoft-word','script','security','shell','video','windows-8'))
AND (q.score >= 0)
AND (q.score <= 1000)

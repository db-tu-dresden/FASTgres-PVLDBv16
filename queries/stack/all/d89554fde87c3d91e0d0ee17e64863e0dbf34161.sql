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
AND (s.site_name in ('askubuntu'))
AND (t.name in ('boot','command-line','dual-boot','installation','kubuntu','nautilus','partitioning','python','suspend','ubuntu-touch','uefi','virtualbox','xorg'))
AND (q.view_count >= 10)
AND (q.view_count <= 1000)

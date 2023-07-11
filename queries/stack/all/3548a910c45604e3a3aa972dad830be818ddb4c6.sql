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
AND (t.name in ('azure-active-directory','bit-manipulation','combinations','connection','css-grid','data-analysis','ftp','geometry','mercurial','navigation-drawer','python-imaging-library','resize','rss','scrollview','wordpress-plugin'))
AND (q.view_count >= 0)
AND (q.view_count <= 100)

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
AND (t.name in ('ado.net','apple-push-notifications','artificial-intelligence','build.gradle','export-to-csv','handlebars.js','href','navbar','navigation-drawer','prepared-statement','query-performance','uiimage','windows-services','word-vba'))
AND (q.view_count >= 0)
AND (q.view_count <= 100)

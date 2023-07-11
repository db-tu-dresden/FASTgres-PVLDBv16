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
AND (t.name in ('argparse','facebook-like','instance','jcombobox','laravel-5.5','libcurl','matlab-figure','mediawiki','multi-tenant','openshift','physics','puppet','rdd','session-variables','video-capture'))
AND (q.score >= 1)
AND (q.score <= 10)

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
AND (t.name in ('android-intent','cakephp-3.0','cocoa-touch','dropdown','dynamics-crm','electron','escaping','grid','html-email','python-3.x','uitableview','woocommerce','xmlhttprequest'))
AND (q.view_count >= 10)
AND (q.view_count <= 1000)

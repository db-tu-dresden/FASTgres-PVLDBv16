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
AND (t.name in ('api','append','combobox','datepicker','dynamic','google-maps-api-3','gridview','html-table','operating-system','python-3.x','ruby-on-rails-5','struct','xml'))
AND (q.view_count >= 0)
AND (q.view_count <= 100)

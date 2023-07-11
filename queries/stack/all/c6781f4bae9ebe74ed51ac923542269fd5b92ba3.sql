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
AND (t.name in ('antlr4','appstore-approval','configuration-files','destructor','distributed-computing','google-adwords','laravel-blade','python-module','quicksort','rtf','wikipedia'))
AND (q.score >= 0)
AND (q.score <= 5)

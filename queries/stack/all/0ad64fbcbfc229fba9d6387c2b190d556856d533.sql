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
AND (t.name in ('ado','angular-routing','babel','boto3','delphi-xe5','dispatcher','file-handling','flash-builder','nsfilemanager','traits','wampserver'))
AND (q.view_count >= 100)
AND (q.view_count <= 100000)

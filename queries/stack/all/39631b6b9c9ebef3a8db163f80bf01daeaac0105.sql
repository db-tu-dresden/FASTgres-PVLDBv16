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
AND (t.name in ('amazon-redshift','bind','carrierwave','crashlytics','httpurlconnection','inputstream','java-web-start','linux-device-driver','openshift','oracle-apex','paramiko','sublimetext','wget'))
AND (q.score >= 1)
AND (q.score <= 10)

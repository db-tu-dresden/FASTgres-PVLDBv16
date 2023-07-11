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
AND (t.name in ('.net-assembly','android-imageview','autofac','core-location','django-queryset','forms-authentication','log4j2','pom.xml','spark-dataframe','sql-injection','system','uialertview','vuex','xdebug','xmpp'))
AND (q.score >= 0)
AND (q.score <= 0)

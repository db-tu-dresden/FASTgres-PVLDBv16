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
AND (t.name in ('alamofire','amazon-cognito','classloader','complexity-theory','database-performance','dependency-properties','ejb-3.0','jhipster','nsfetchedresultscontroller','positioning','rcpp','refresh','session-cookies','string-formatting','symfony-1.4'))
AND (q.score >= 1)
AND (q.score <= 10)

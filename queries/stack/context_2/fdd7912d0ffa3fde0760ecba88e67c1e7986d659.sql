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
AND (s.site_name in ('stats'))
AND (t.name in ('conditional-probability','covariance','data-transformation','dataset','deep-learning','expected-value','experiment-design','mean','nonparametric','poisson-distribution','predictive-models','random-forest','simulation','terminology'))
AND (q.view_count >= 10)
AND (q.view_count <= 1000)

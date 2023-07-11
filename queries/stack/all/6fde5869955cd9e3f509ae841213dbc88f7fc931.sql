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
AND (t.name in ('anova','arima','clustering','cross-validation','data-visualization','deep-learning','estimation','generalized-linear-model','maximum-likelihood','multiple-regression','references','statistical-significance','variance'))
AND (q.favorite_count >= 0)
AND (q.favorite_count <= 10000)

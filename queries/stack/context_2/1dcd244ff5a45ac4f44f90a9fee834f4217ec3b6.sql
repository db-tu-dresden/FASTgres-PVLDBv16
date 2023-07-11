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
AND (s.site_name in ('mathoverflow'))
AND (t.name in ('algebraic-number-theory','analytic-number-theory','cv.complex-variables','differential-topology','ds.dynamical-systems','finite-groups','homotopy-theory','inequalities','lie-groups','measure-theory','mp.mathematical-physics','oa.operator-algebras','probability-distributions','st.statistics','stochastic-processes'))
AND (q.view_count >= 10)
AND (q.view_count <= 1000)

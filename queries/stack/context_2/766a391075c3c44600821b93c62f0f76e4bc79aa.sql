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
AND (s.site_name in ('physics'))
AND (t.name in ('astronomy','astrophysics','electricity','electrons','everyday-life','inertial-frames','nuclear-physics','orbital-motion','potential','schroedinger-equation','space-expansion','standard-model','supersymmetry','terminology'))
AND (q.score >= 1)
AND (q.score <= 10)

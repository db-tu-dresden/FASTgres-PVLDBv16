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
AND (t.name in ('classical-mechanics','electromagnetism','electrostatics','forces','general-relativity','homework-and-exercises','newtonian-gravity','newtonian-mechanics','quantum-field-theory','special-relativity','thermodynamics'))
AND (q.favorite_count >= 0)
AND (q.favorite_count <= 1)

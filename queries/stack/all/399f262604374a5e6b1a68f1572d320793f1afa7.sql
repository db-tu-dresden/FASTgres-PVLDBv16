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
AND (s.site_name in ('math'))
AND (t.name in ('axiom-of-choice','distribution-theory','epsilon-delta','fourier-series','graphing-functions','inner-product-space','inverse','irreducible-polynomials','laplace-transform','lie-algebras','numerical-linear-algebra','residue-calculus','transformation'))
AND (q.view_count >= 100)
AND (q.view_count <= 100000)

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
AND (t.name in ('ac.commutative-algebra','analytic-number-theory','dg.differential-geometry','gt.geometric-topology','lo.logic','matrices','nt.number-theory','pr.probability','ra.rings-and-algebras','reference-request','rt.representation-theory'))
AND (q.view_count >= 100)
AND (q.view_count <= 100000)

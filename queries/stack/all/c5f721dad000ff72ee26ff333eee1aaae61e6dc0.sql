SELECT t1.name, count(*)
FROM
site as s,
so_user as u1,
question as q1,
answer as a1,
tag as t1,
tag_question as tq1
WHERE
q1.owner_user_id = u1.id
AND a1.question_id = q1.id
AND a1.owner_user_id = u1.id
AND s.site_id = q1.site_id
AND s.site_id = a1.site_id
AND s.site_id = u1.site_id
AND s.site_id = tq1.site_id
AND s.site_id = t1.site_id
AND q1.id = tq1.question_id
AND t1.id = tq1.tag_id
AND (s.site_name in ('mathoverflow'))
AND (t1.name in ('ac.commutative-algebra','co.combinatorics','gn.general-topology','gr.group-theory','graph-theory','lo.logic','real-analysis','reference-request','rt.representation-theory'))
AND (q1.favorite_count >= 0)
AND (q1.favorite_count <= 10000)
AND (u1.reputation >= 0)
AND (u1.reputation <= 100)
GROUP BY t1.name
SELECT acc.location, count(*)
FROM
site as s,
so_user as u1,
question as q1,
answer as a1,
tag as t1,
tag_question as tq1,
badge as b,
account as acc
WHERE
s.site_id = q1.site_id
AND s.site_id = u1.site_id
AND s.site_id = a1.site_id
AND s.site_id = t1.site_id
AND s.site_id = tq1.site_id
AND s.site_id = b.site_id
AND q1.id = tq1.question_id
AND q1.id = a1.question_id
AND a1.owner_user_id = u1.id
AND t1.id = tq1.tag_id
AND b.user_id = u1.id
AND acc.id = u1.account_id
AND (s.site_name in ('askubuntu','math'))
AND (t1.name in ('abstract-algebra','analysis','combinations','command-line','determinant','finite-groups','general-topology','graph-theory','logarithms','polynomials','power-series','prime-numbers','random-variables','reference-request','systems-of-equations'))
AND (q1.view_count >= 0)
AND (q1.view_count <= 100)
AND (u1.downvotes >= 0)
AND (u1.downvotes <= 1)
AND (b.name in ('Cleanup','Constituent','Enlightened','Enthusiast','Fanatic','Good Answer','Great Question','Investor','Mortarboard','Organizer','Peer Pressure','Self-Learner','Talkative','Vox Populi'))
GROUP BY acc.location
ORDER BY COUNT(*)
DESC
LIMIT 100

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
AND (s.site_name in ('codereview'))
AND (t.name in ('algorithm','array','beginner','c++','c++11','game','java','jquery','multithreading','php','programming-challenge','python','sql','strings'))
AND (q.score >= 1)
AND (q.score <= 10)

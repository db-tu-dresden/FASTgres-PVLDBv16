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
AND (s.site_name in ('stackoverflow'))
AND (t.name in ('c++17','guava','gulp','html5-video','mingw','onclick','singleton','sublimetext3','subprocess','testng','themes','timestamp','typo3','x86-64','xss'))
AND (q.favorite_count >= 1)
AND (q.favorite_count <= 10)

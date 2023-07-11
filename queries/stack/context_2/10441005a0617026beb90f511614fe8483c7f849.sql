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
AND (s.site_name in ('rpg'))
AND (t.name in ('balance','character-creation','dungeons-and-dragons','homebrew','optimization','skills','weapons'))
AND (q.score >= 0)
AND (q.score <= 1000)

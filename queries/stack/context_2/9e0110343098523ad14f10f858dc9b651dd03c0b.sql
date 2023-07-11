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
AND (s.site_name in ('english'))
AND (t.name in ('adverbs','antonyms','articles','british-english','commas','conjunctions','idiom-requests','phrase-meaning','pronouns','pronunciation','syntactic-analysis','tenses','vocabulary','word-order','writing-style'))
AND (q.score >= 0)
AND (q.score <= 1000)

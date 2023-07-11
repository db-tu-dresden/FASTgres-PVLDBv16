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
AND (s.site_name in ('magento'))
AND (t.name in ('admin','adminhtml','attributes','cart','configurable-product','customer','error','magento-1','magento-1.7','magento-1.8','magento-1.9','magento-2.1','module','php','product-attribute'))
AND (q.score >= 0)
AND (q.score <= 1000)

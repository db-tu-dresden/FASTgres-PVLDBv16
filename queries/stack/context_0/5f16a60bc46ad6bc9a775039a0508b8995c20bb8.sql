SELECT b1.name, count(*)
FROM
site as s,
so_user as u1,
tag as t1,
tag_question as tq1,
question as q1,
badge as b1,
account as acc
WHERE
s.site_id = u1.site_id
AND s.site_id = b1.site_id
AND s.site_id = t1.site_id
AND s.site_id = tq1.site_id
AND s.site_id = q1.site_id
AND t1.id = tq1.tag_id
AND q1.id = tq1.question_id
AND q1.owner_user_id = u1.id
AND acc.id = u1.account_id
AND b1.user_id = u1.id
AND (q1.view_count >= 100)
AND (q1.view_count <= 100000)
AND (s.site_name in ('es','pt','ru','superuser'))
AND (t1.name in ('audio','batch-file','bookmarks','connection','fan','javafx','lcd','microsoft-excel-2007','privacy','qt','uefi','windows-subsystem-for-linux','wireless-access-point','zsh'))
AND (acc.website_url like ('%code%'))
GROUP BY b1.name
ORDER BY COUNT(*)
DESC
LIMIT 100

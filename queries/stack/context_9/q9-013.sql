
select count(distinct account.id) from
account, site, so_user, question q, post_link pl, tag, tag_question tq where
not exists (select * from answer a where a.site_id = q.site_id and a.question_id = q.id) and
site.site_name = 'stackoverflow' and
site.site_id = q.site_id and
pl.site_id = q.site_id and
pl.post_id_to = q.id and

tag.name = 'codeigniter' and
tag.site_id = q.site_id and

q.creation_date > '2016-01-01'::date and

tq.site_id = tag.site_id and
tq.tag_id = tag.id and
tq.question_id = q.id and

q.owner_user_id = so_user.id and
q.site_id = so_user.site_id and
so_user.reputation > 126 and

account.id = so_user.account_id and
account.website_url != '';

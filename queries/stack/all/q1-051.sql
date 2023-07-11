
select count(*) from tag, site, question, tag_question
where
site.site_name='stackoverflow' and
tag.name='dynamics-ax-2012-r2' and
tag.site_id = site.site_id and
question.site_id = site.site_id and
tag_question.site_id = site.site_id and
tag_question.question_id = question.id and
tag_question.tag_id = tag.id

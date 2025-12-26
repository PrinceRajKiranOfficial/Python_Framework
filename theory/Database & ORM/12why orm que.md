12. Why ORM Queries are Easy to Read

SQL (Hard)
    SELECT * FROM post WHERE id = 1;

Django ORM (Easy)
    post.objects.get(id=1)

& Looks like English + Python




13. CRUD Operations Concept


Operation | Meaning | ORM Example
Create | Add data | create ( )
Read | Fetch data | all(), get(), filter()
Update | Modify data | save ( )
Delete | Remove data | delete()
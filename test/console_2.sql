select name
from books
where status = 'Borrowed';

--alter table users
--    drop column age;

delete
from users;

select book_id, user_id,(select name from users where id = main.user_id) as User_Name,
       (select name from books where id = main.book_id) as book_name,
       borrow_date,
       --(select count(book_id) from operations where book_id=48) as count
       (select count(book_id) from operations where book_id=main.book_id) as count
from operations main
where borrow_date between '2022/1/1' and '2022/12/31'
order by count desc; --limit 1;

select count(book_id) from operations where book_id=48;
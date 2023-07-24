import sqlite3

conn = sqlite3.connect(r'C:\Users\yosse\PycharmProjects\pythonProject1\library system\db')
c = conn.cursor()


def account():
    j = open("members_account", "r")
    print("Open an account")
    id = 0
    last = j.readlines()
    if last:
        id = int(last[-1][0])
    id += 1
    j.close()
    name = input("name:")
    dob = input("dob:")
    telephone_number = input("telephone_number:")
    j = open("members_account", "a")
    if name.isalpha() and telephone_number.isdigit() and dob.isdigit():
        j.write(f"""{id},{name},{dob},{telephone_number}\n""")
        j.close()
    else:
        print("Invalid input")


def search_book():
    name = input("enter book programming name or id:")
    c.execute(f"SELECT * FROM books where name like '%{name}%'")
    rows = c.fetchall()
    if rows:
        for row in rows:
            print(row)
        c.close()
        conn.close()
    else:
        print("Invalid book")


def checkout():
    user_id = input("enter your id:")
    c.execute(f"SELECT id FROM member_data where id = {user_id}")
    rows = c.fetchall()
    import datetime
    now = datetime.datetime.now()
    if rows:
        book_id = input("choice id you want:")
        c.execute(f"SELECT id FROM books where id = {book_id} and status ='Available'")
        rows = c.fetchall()
        if rows:
            c.execute(f"update books set status = 'Borrowed' where id={book_id}")
            c.execute(f"update books set borrower_id ='{user_id}'  where id={book_id}")

            c.execute(
                f"insert into operation (book_id, user_id ,borrow_date,expected_return_date) values ({book_id},{user_id},date ('now'),date('now', '+7 days'));")
            conn.commit()
        else:
            print("Invalid book")
    else:
        print("Invalid id")


def return_book():
    user_id = input("enter your id:")
    c.execute(f"SELECT id FROM member_data where id = {user_id}")
    rows = c.fetchall()
    if rows:
        book_id = input("choice id you want:")
        c.execute(f"SELECT id FROM books where id = {book_id} and status ='Borrowed'")
        rows = c.fetchall()
        if rows:
            c.execute(f"update books set status = 'Available'  , borrower_id =Null where id={book_id}")
            c.execute(f"""
            update operation 
            set actual_return_date = date ('now')
              where actual_return_date is Null and user_id={user_id} and book_id={book_id};
            """)

            conn.commit()

        else:
            print("Invalid book")
    else:
        print("Invalid id")


while True:
    print("what you want \n1-create account.\n2-search book\n3-checkout book\n4-return book")
    choice = input("enter you choice:")
    if choice.isdigit():
        choice = int(choice)
        if choice == 1:
            account()
        elif choice == 2:
            search_book()
        elif choice == 3:
            checkout()
        elif choice == 4:
            return_book()

    else:
        print("Invalid Choice")

# for row in rows:
#     print(row)
# c.close()
# conn.close()

from flask import Flask, render_template, request, redirect, session
import sqlite3, datetime

# users.html
app = Flask(__name__)
app.secret_key = '123'


def handle_db(sql):
    conn = sqlite3.connect(r'C:\Users\yosse\PycharmProjects\pythonProject1\library system\db')
    cursor = conn.cursor()
    cursor.execute(sql)
    if sql.lower().startswith('select'):
        col_names = [i[0] for i in cursor.description]
        result = cursor.fetchall()
        return col_names, result
    else:
        conn.commit()
    cursor.close()
    conn.close()


@app.route('/')
def start():
    if not session:
        if request.args:
            email = request.args["email"]
            password = request.args["password"]
            login = handle_db(
                f"select id,name,email,password ,type from users where email='{email}' and password= '{password}'")
            if login:
                session['id'] = login[1][0][0]
                session['name'] = login[1][0][1]
                session['email'] = login[1][0][2]
                session['type'] = login[1][0][4]
                if login[1][0][4] == 'admin':
                    return render_template('page_admin.html', x=session['name'])
                else:
                    return render_template('users.html', x=session['name'])

        else:
            return render_template('login.html')
    else:
        if session['type'] == 'admin':
            return render_template('page_admin.html',x=session['name'])
        else:
            return render_template('users.html',x=session['name'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/create_member')
def member():
    if request.args:
        name = request.args["name"]
        dob = request.args["dob"]
        email = request.args["email"]
        password = request.args["password"]
        next_id = handle_db('SELECT max(id)+1 FROM users ')
        next_id = next_id[0][0]
        sql = f"insert into users (id, name ,dob,email,password) values ({next_id},'{name}','{dob}','{email}','{password}')"
        handle_db(sql)
        return render_template('users.html')
    else:
        return render_template('create_member.html')


@app.route('/books')
def book():
    if request.args:
        name = request.args['name']
        book_names = handle_db(f"SELECT id,name FROM books where name like '%{name}%'")
        return render_template('results.html', results=book_names, x="books")
    else:
        return render_template('search_book.html')


@app.route('/all_members')
def all_members():
    members = handle_db(f"select name from users")
    return render_template("results.html", results=members, x="members")


@app.route('/all_books')
def all_books():
    books = handle_db(f"select id,name from books")
    return render_template("results.html", results=books, x="books")


@app.route('/checkout')
def checkout():
    if request.args:
        user_id = session['id']
        now = datetime.datetime.now()
        if user_id:
            # member_id = member_id[0][0]
            book_id = request.args["book id"]
            book_id = handle_db(f"SELECT id FROM books where id = {book_id} and status ='Available'")
            if book_id:
                book_id = book_id[1][0][0]
                handle_db(f"update books set status = 'Borrowed' where id={book_id}")
                handle_db(f"update books set borrower_id ='{user_id}'  where id={book_id}")
                handle_db(
                    f"insert into operations (book_id, user_id ,borrow_date,expected_return_date) values ({book_id},{user_id},date ('now'),date('now', '+7 days'));")
            else:
                print("Invalid book")
        else:
            print("Invalid id")
        return render_template("users.html")
    else:
        return render_template("check_out.html")


@app.route('/return_book')
def return_books():
    user_id = session['id']
    if request.args:
        if user_id:
            book_id = request.args["book id"]
            book_id = handle_db(f"SELECT id FROM books where id = {book_id} and status ='Borrowed'")
            if book_id:
                book_id = book_id[1][0][0]
                handle_db(f"update books set status = 'Available'  , borrower_id =Null where id={book_id}")
                handle_db(f"""
                    update operations 
                    set actual_return_date = date ('now')
                      where actual_return_date is Null and user_id={user_id} and book_id={book_id};
                    """)
            else:
                print("Invalid book")
        else:
            print("Invalid id")
        return render_template("users.html")
    else:
        borrower_book = handle_db(f"SELECT id,name FROM books where borrower_id ={user_id} and status ='Borrowed'")

        return render_template("return_book.html", results=borrower_book, x='books you borrowe')


@app.route('/Borrower_books')
def Borrower_books():
    books = handle_db(f"select id,name from books where status ='Borrowed'")
    return render_template("results.html", results=books, x="Borrowed books")


@app.route('/Available_books')
def Available_books():
    books = handle_db(f"select id,name from books where status ='Available'")
    return render_template("results.html", results=books, x="Available books")


@app.route('/The_most_borrowed_book')
def The_most_borrowed_book():
    if request.args:
        date_from = request.args['date_from'].replace('-', '/')
        date_to = request.args['date_to'].replace('-', '/')
        sql = f"""select book_id,
           (select name from books where id = main.book_id)  as book_name,
           (select count(book_id) from operations where book_id = main.book_id) as count ,
            borrow_date
            from operations main
            where borrow_date between '{date_from}' and '{date_to}'   
            order by count desc limit 1
                    """
        book = handle_db(sql)
        return render_template("results.html", results=book, x="The_most_borrowed_book")
    else:
        return render_template('input_date.html')


@app.route('/The_least_borrowed_book')
def The_least_borrowed_book():
    if request.args:
        date_from = request.args['date_from'].replace('-', '/')
        date_to = request.args['date_to'].replace('-', '/')
        sql = f"""select book_id,
           (select name from books where id = main.book_id)  as book_name,
           (select count(book_id) from operations where book_id = main.book_id) as count ,
            borrow_date
            from operations main
            where borrow_date between '{date_from}' and '{date_to}'   
            order by count asc limit 1
                    """
        book = handle_db(sql)
        return render_template("results.html", results=book, x="The_least_borrowed_book")
    else:
        return render_template('input_date.html')


# @app.route('/')
# def add_book():
#     name = request.args["name"]
#     next_id = handle_db('SELECT max(id)+1 FROM users ')
#     next_id = next_id[0][0]
#     f = open('dob.csv', 'r')
#     lines = f.readlines()
#     for line in lines:
#         line = line.split(',')
#         sql = f"""
#         insert into operations (user_id,book_id, borrow_date,expected_return_date, actual_return_date) values ({line[0]},{line[1]},'{line[2]}','{line[3]}','{line[4].strip()}')
#         """
#         handle_db(sql)
#
#     return


if __name__ == '__main__':
    app.run(port=80)

from flask import Flask, render_template, request
import sqlite3, datetime
app = Flask(__name__)
@app.route('/')
def start():
    return "welcome"


@app.route('/number')
def numbers():
    r = request
    sum = int(r.args['x']) + int(r.args['y'])

    return str(sum)
    # return str("hello")



@app.route('/random')
def r():
    import random
    x = random.randint(1, 100)
    return str(f"""
    <center>
    <h1>Welcome to random numbers service \n
    <hr>
    
     {x} </h1>
     
     <a href="/temp/zagazig">go to temp zag </a>
    </center>
    """)


@app.route('/time')
def r_color():
    import datetime
    x = datetime.datetime.now()
    return str(f"Welcome to random numbers service \n {x}")

@app.route('/books')
def book():
    import sqlite3

    conn = sqlite3.connect(r'C:\Users\yosse\PycharmProjects\pythonProject1\library system\db')
    c = conn.cursor()

    name = request.args['name']
    c.execute(f"SELECT name FROM books where name like '%{name}%'")
    rows = c.fetchall()
    if rows:
        x = ""
        for row in rows:
            x = x + f"<li>{row[0]}"
        c.close()
        conn.close()
    else:
        print("Invalid book")
    return str(f"""
    <ol>
    {x}
    </ol>
""")
@app.route('/create_member')
def member():
    import sqlite3
    conn = sqlite3.connect(r'C:\Users\yosse\PycharmProjects\pythonProject1\library system\db')
    c = conn.cursor()
    name=request.args["name"]
    dob=request.args["dob"]
    c.execute('SELECT max(id)+1 FROM users ')
    next_id = c.fetchone()[0]
    insert_statement=f"insert into users (id, name ,dob) values ({next_id},'{name}','{dob}')"
    c.execute(insert_statement)
    conn.commit()
    c.close()
    conn.close()
    return 'thank you'
@app.route('/checkout')
def checkout():
    conn = sqlite3.connect(r'C:\Users\yosse\PycharmProjects\pythonProject1\library system\db')
    c = conn.cursor()


    user_id=request.args["user id"]
    c.execute(f"SELECT id FROM users where id = {user_id}" )
    member_id = c.fetchall()

    now = datetime.datetime.now()
    if member_id:
        member_id = member_id[0][0]
        book_id = request.args["book id"]
        c.execute(f"SELECT id FROM books where id = {book_id} and status ='Available'")
        book_id = c.fetchall()
        if book_id:
            book_id=book_id[0][0]
            c.execute(f"update books set status = 'Borrowed' where id={book_id}")
            c.execute(f"update books set borrower_id ='{user_id}'  where id={book_id}")

            c.execute(
                f"insert into operation (book_id, user_id ,borrow_date,expected_return_date) values ({book_id},{user_id},date ('now'),date('now', '+7 days'));")
            conn.commit()
        else:
            print("Invalid book")
    else:
        print("Invalid id")
    return 'check out success'

@app.route('/return_book')
def return_books():
    conn = sqlite3.connect(r'C:\Users\yosse\PycharmProjects\pythonProject1\library system\db')
    c = conn.cursor()
    user_id = request.args["user id"]

    c.execute(f"SELECT id FROM member_data where id = {user_id}")
    member_id = c.fetchall()
    if member_id:
        member_id=member_id[0][0]
        book_id = request.args["book id"]
        c.execute(f"SELECT id FROM books where id = {book_id} and status ='Borrowed'")
        book_id = c.fetchall()
        if book_id:
            book_id=book_id[0][0]
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
    return 'return book success'

if __name__ == '__main__':
    app.run(port=80)

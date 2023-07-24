import sqlite3

conn = sqlite3.connect(r'C:\Users\yosse\PycharmProjects\pythonProject1\library system\db')
c = conn.cursor()
# # Fill users
# f = open('random_data.csv', 'r')
# lines = f.readlines()
# c.execute("delete from users;")
# for line in lines:
#     line = line.split(',')
#     sql = f"""
#     insert into users (id, name, dob,email, password,  type) values ({line[0]},'{line[1]}','{line[2]}','{line[3]}','{line[4]}','{line[5].strip()}')
#     """
#     print(sql)
#     c.execute(sql)
#     conn.commit()
#fill operations
f = open('dob.csv', 'r')
lines = f.readlines()
c.execute("delete from operations;")
for line in lines:
    line = line.split(',')
    sql = f"""
    insert into operations (user_id,book_id, borrow_date,expected_return_date, actual_return_date) values ({line[0]},{line[1]},'{line[2]}','{line[3]}','{line[4].strip()}')
    """
    print(sql)
    c.execute(sql)
    conn.commit()
c.close()
conn.close()

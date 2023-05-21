import apps.dbconnect as db

def addfewemployees():
    
    sqlcode = """ INSERT INTO employees(
        employee_ln,
        employee_fn,
        employee_role,
        employee_modified_date,
        employee_delete_ind
    )
    VALUES (%s, %s, %s, %s, %s)"""

    from datetime import datetime
    
    db.modifydatabase(sqlcode, ['Benigno', 'Myrrh', 'faculty', datetime.now(), False])
    db.modifydatabase(sqlcode, ['Boco', 'Zyrene', 'student', datetime.now(), False])
    print('done!')

sql_query = """SELECT * FROM employees"""
values=[]
columns = ['id', 'ln', 'fn', 'role', 'modified', 'is_deleted']
df = db.querydatafromdatabase(sql_query, values, columns)
print(df)

sql_resetemployees = """
 TRUNCATE TABLE employees RESTART IDENTITY CASCADE
"""
db.modifydatabase(sql_resetemployees, [])
addfewemployees()
df = db.querydatafromdatabase(sql_query, values, columns)
print(df)
from django.db import connection

def dictfetchall(cursor):
    rows = cursor.fetchall()
    if(not rows):
        return []
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in rows]

def sqlquery(sql):
    # print(sql)
    # get the cursor
    cursor = connection.cursor()
    # execute the command
    cursor.execute(sql)
    # get all data
    data = dictfetchall(cursor)
    # close the cursor
    cursor.close()
    # return the data
    # print("run sql successfully")
    return data

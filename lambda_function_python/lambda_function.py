from datetime import datetime
import os
import psycopg2

con = None
#query = ''

def lambda_handler(event, context):
    print('Scheduled maintenance started at {}'.format(str(datetime.now())))
    print(event)
    try:
        host = "businstance.c4lkxc6noi6m.us-east-1.rds.amazonaws.com"
        database = "busdb"
        user = "testrole"
        password = "argolabs"

        con = psycopg2.connect(host=host, database=database, user=user, password=password)
        cur = con.cursor()
        cur.execute('SELECT * FROM devicelocation')
        rows = cur.fetchall()
        print(rows)


    except psycopg2.DatabaseError as e:
        print('Error: {}'.format(e))
        raise
    else:
        print('done!')
    finally:
        print('completed at {}'.format(str(datetime.now())))
        if con:
            con.close()

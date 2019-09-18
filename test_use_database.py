from DBcm import UseDatabase

dbconfig = {'host': '127.0.0.1',
            'user': 'vsearch',
            'password': 'quakA!',
            'database': 'vsearchlogDB', }

with UseDatabase(dbconfig) as cursor:
    sql = """show tables"""
    cursor.execute(sql)
    data = cursor.fetchall()

data

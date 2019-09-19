from db_cm import UseDatabase
from flask import escape

dbconfig = {'host': '127.0.0.1',
            'user': 'vsearch',
            'password': 'quakA!',
            'database': 'vsearchlogDB', }

with UseDatabase(dbconfig) as cursor:
    sql = """show tables"""
    cursor.execute(sql)
    data = cursor.fetchall()

data

# %%
contents = [("1","2","<script></script>"),
            ("<script></script>", "<>", "&")]

contents_escaped = [[escape(entry) for entry in tuple] for tuple in contents]

# %%
contents_escaped
# %%
type(contents[0])

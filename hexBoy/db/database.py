# import sqlite3

from sqlalchemy import create_engine, inspect, text

connectionPath = 'hexBoy/db/hex_sqlite.db'
connectionString = 'sqlite:///' + connectionPath

engine = create_engine(connectionString, echo=True)
print(type(engine))

# print table names, I don't think I ever care unless to test I guess
insp = inspect(engine)
print(insp.get_table_names())


with engine.connect() as con: 
    result = con.execute(text("SELECT * FROM movie LIMIT 10"))

    first_result = result.fetchone()
    print(type(first_result))
    print(first_result)
    print(first_result['name'])

    







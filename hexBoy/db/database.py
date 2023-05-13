import sqlite3
from sqlalchemy import create_engine

engine = create_engine('sqlite:///hex_sqlite.db')

engine.table_names()
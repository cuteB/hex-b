# import sqlite3

from typing import List, Optional
from sqlalchemy import create_engine, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

connectionPath = 'hexBoy/db/hex_sqlite.db'
connectionString = 'sqlite:///' + connectionPath

engine = create_engine(connectionString, echo=True)
print(type(engine))

# import sqlite3

from typing import List, Optional
from sqlalchemy import create_engine, ForeignKey, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

connectionPath = 'hexBoy/db/hex_sqlite.db'
connectionString = 'sqlite:///' + connectionPath

engine = create_engine(connectionString) # use 'echo = true' parameter for all of the print statements
# echo parameter adds the sql representation of the queries to the console


# This is just a test file to see how to do stuff
# This is just a test file to see how to do stuff
# This is just a test file to see how to do stuff
# This is just a test file to see how to do stuff
# This is just a test file to see how to do stuff

'''---
Copy Pasted these two
---'''
# can also do Base = DeclarativeBase
class Base(DeclarativeBase):
    pass

class User(Base):
    #  Table Name
    __tablename__ = "user_account"

    # Column Definitions
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]

    # Relationship Definitions
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    # Print Method for when the object is returned or printed
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))

    user: Mapped["User"] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return (f"Address(id={self.id!r}, email_address={self.email_address!r}") 

# create table
Base.metadata.create_all(engine)

# Sessions are used to run queries and interact with the database
with Session(engine) as session:

    # start cleanup
    stmt = select(User)
    for user in session.scalars(stmt):
        session.delete(user)
    session.commit()
    # end cleanup

    # write
    spongebob = User(
        name="spongebob", 
        fullname="Spongebob Squarepants",
        addresses=[Address(email_address="spongebob@sqlalchemy.org")]
    )
    sandy = User(
        name="sandy",
        fullname="Sandy Cheeks",
        addresses=[
            Address(email_address="sandy@sqlalchemy.org"),
            Address(email_address="sandy@squirrelpower.org"),
        ],
    )
    patrick = User(name="patrick", fullname="Patrick Star")

    print(sandy) # id = none

    session.add_all([spongebob, sandy, patrick])
    session.commit()

    print(sandy) # id is now set. 

    # read
    stmt = select(User).where(User.name.in_(["spongebob", "sandy"]))

    for user in session.scalars(stmt):
        print(user)

    # join
    stmt = (
        select(Address)
        .join(Address.user)
        .where(User.name == "sandy")
        .where(Address.email_address == "sandy@sqlalchemy.org")
    )

    sandy_address = session.scalars(stmt).one()
    print(sandy_address) # id = none


    # update
    stmt = select(User).where(User.name == "patrick")
    patrick = session.scalars(stmt).one()
    patrick.addresses.append(Address(email_address="patrickstar@sqlalchemy.org"))

    sandy_address.email_address = "sandy_cheeks@sqlalchemy.org"

    session.commit()


    # delete
    sandy = session.get(User,2)
    sandy.addresses.remove(sandy_address)

    print(sandy) # id is set once record is written/read from the database

    session.delete(patrick)
    session.commit()


    



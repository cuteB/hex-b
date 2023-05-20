# import sqlite3

from hexBoy.hex.node.HexNode import Hex
from typing import List, Optional
from sqlalchemy import create_engine, ForeignKey, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

class Base(DeclarativeBase):
    pass

'''---
Game
---'''
class Game(Base):
    __tablename__ = "hex_game"

    id: Mapped[int] = mapped_column(primary_key=True)
    blueAgent: Mapped[str]
    redAgent: Mapped[str]
    winner: Mapped[Optional[str]]

    moves: Mapped[List["Move"]] = relationship(
        back_populates="game", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Game(id={self.id!r}, blueAgent={self.blueAgent!r}, redAgent={self.redAgent!r}, winner={self.winner!r})"

'''---
Move
---'''
class Move(Base):
    __tablename__ = "game_move"

    id: Mapped[int] = mapped_column(primary_key=True)
    player: Mapped[int]
    move: Mapped[tuple]

    game: Mapped["Game"] = relationship(back_populates="moves")

    def __repr__(self) -> str:
        return (f"Move(id={self.id!r}, player={self.player!r}, move={self.move!r})") 
    


def initDB() -> None:
    connectionPath = 'hexBoy/db/hex_sqlite.db' # TODO there is some garbage tables still in here
    connectionString = 'sqlite:///' + connectionPath

    engine = create_engine(connectionString) # use 'echo = true' parameter for all of the print statements
    # echo parameter adds the sql representation of the queries to the console



    Base.metadata.create_all(engine)

    # Open DB Session
    with Session(engine) as session:

        # cleanup
        query = select(Game)
        for g in session.scalars(query):
            session.delete(g)
        session.commit()


        testGame = Game(
            blueAgent = "bran",
            redAgent = "Agent_Rand"
        )

        session.add(testGame)

        print(testGame)

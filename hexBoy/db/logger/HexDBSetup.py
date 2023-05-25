# import sqlite3

from hexBoy.hex.node.HexNode import Hex
from typing import List, Optional
from sqlalchemy import create_engine, ForeignKey, String, select, Engine
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
    game_id: Mapped[int] = mapped_column(ForeignKey("hex_game.id"))
    game: Mapped["Game"] = relationship(back_populates="moves")
    player: Mapped[int]
    x: Mapped[int] 
    y: Mapped[int]

    sequence: Mapped[int]

    def __init__(self, player: int, move: Hex, sequence: int):
        self.player = player
        self.x, self.y = move 
        self.sequence = sequence




    def __repr__(self) -> str:
        return (f"Move(id={self.id!r}, gameId={self.game_id!r}, player={self.player!r}, move=({self.x!r},{self.y!r}), sequence={self.sequence!r})") 


class DBManager:
    connectionPath = 'hexBoy/db/hex_sqlite.db' # TODO there is some garbage tables still in here
    connectionString = 'sqlite:///' + connectionPath
    engine: Engine

    currentGame: Game
    currentGameId: int
    gameSequence: int

    def __init__(self):
        self.engine = create_engine(self.connectionString)

    def resetDB(self):
        Game.__table__.drop(self.engine)
        Move.__table__.drop(self.engine)

    def initDBTables(self) -> None:
        Base.metadata.create_all(self.engine)


    def startGame(self, blueAgent: str, redAgent: str):
        currentGame = Game(
            blueAgent = blueAgent,
            redAgent = redAgent
        )
        self.gameSequence = 0 # IDK if this should be inside here

        with Session(self.engine) as session:
            session.add(currentGame)
            session.commit()
            self.currentGameId = currentGame.id

    def addMove(self, player, move):

        with Session(self.engine) as session: 
            m = Move(player, move, self.gameSequence)
            query = (
                select(Game)
                .where(Game.id == self.currentGameId)
            )
            currentGame = session.scalars(query).one()
            currentGame.moves.append(m)
            session.commit()
            self.gameSequence += 1

    def printMoveForGame(self):
        with Session(self.engine) as session:
            query = (
                select(Move)
                .where(Move.game_id == self.currentGameId)
            )

            for m  in session.scalars(query):
                print(m, m.x, m.y)


def initDB() -> None:
    dbm = DBManager()

    dbm.resetDB()
    dbm.initDBTables()

    dbm.startGame("blue", "red")

    dbm.addMove(1, (5,5))
    dbm.addMove(2, (5,6))
    dbm.addMove(1, (5,7))
    dbm.addMove(2, (5,8))
    dbm.addMove(1, (5,9))
    dbm.addMove(2, (5,10))

    dbm.printMoveForGame()

# import sqlite3

from hexBoy.hex.node.HexNode import Hex
from typing import List, Optional
from sqlalchemy import create_engine, ForeignKey, String, select, Engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

'''
[ ] I think I want to add the time to the logs
'''

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
    winner: Mapped[Optional[int]]

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


class HexLogger:
    connectionPath = 'hexBoy/db/hex_sqlite.db' # TODO there is some garbage tables still in here
    connectionString = 'sqlite:///' + connectionPath
    engine: Engine

    currentGame: Game
    currentGameId: int
    gameSequence: int
    gameInProgress: bool # COMEBACK I might want to merge this with the currentGameId to track if a game is in progress

    def __init__(self):
        self.engine = create_engine(self.connectionString)
        self.gameInProgress = False

    def resetDB(self):
        Game.__table__.drop(self.engine)
        Move.__table__.drop(self.engine)

    def initDBTables(self) -> None:
        Base.metadata.create_all(self.engine)


    def logStartGame(self, blueAgent: str, redAgent: str) -> None:
        """"""
        currentGame = Game(
            blueAgent = blueAgent,
            redAgent = redAgent
        )
        self.gameSequence = 0 # IDK if this should be inside here
        self.gameInProgress = True

        with Session(self.engine) as session:
            session.add(currentGame)
            session.commit()
            self.currentGameId = currentGame.id

    def logMove(self, player: int, move: Hex) -> None:

        if (not self.gameInProgress):
            return # COMEBACK do I want this? I might want this to fail or say something 

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

    def logEndGame(self, winnerId: int) -> None:
        self.gameInProgress = False

        with Session(self.engine) as session:
            query = (
                select(Game)
                .where(Game.id == self.currentGameId)
            )

            g = session.scalars(query).one()
            g.winner = winnerId

            session.commit()

    def printMoveForGame(self) -> None:
        with Session(self.engine) as session:
            query = (
                select(Move)
                .where(Move.game_id == self.currentGameId)
            )

            for m in session.scalars(query):
                print(m, m.x, m.y)

            query = (
                select(Game)
                .where(Game.id == self.currentGameId)
            )

            g = session.scalars(query).one()
            print(g)

def initDB() -> None:
    xLogger = HexLogger()

    xLogger.resetDB()
    xLogger.initDBTables()

    xLogger.logStartGame("blue", "red")

    xLogger.logMove(2, (5,6))
    xLogger.logMove(1, (5,7))
    xLogger.logMove(1, (5,5))
    xLogger.logMove(2, (5,8))
    xLogger.logMove(1, (5,9))
    xLogger.logMove(2, (5,10))

    xLogger.printMoveForGame()

    xLogger.logEndGame(1)

    xLogger.printMoveForGame()

    xLogger.logStartGame("one", "two")

    xLogger.logMove(2, (5,6))
    xLogger.logMove(1, (5,7))
    xLogger.logMove(1, (5,5))
    xLogger.logMove(2, (5,8))
    xLogger.logMove(1, (5,9))
    xLogger.logMove(2, (5,10))


    xLogger.logEndGame(2)

    xLogger.printMoveForGame()
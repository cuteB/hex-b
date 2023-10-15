# TODO probably rename this file and create a setup file that is separate from the logger

# import sqlite3 

from hexBoy.hex.node.HexNode import Hex
from typing import List, Optional
from sqlalchemy import create_engine, ForeignKey, String, select, Engine, asc
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

'''
[ ] I think I want to add the time to the logs
[ ] create logger interface so I can swap out the DB later
[ ] A GameHistory table that tracks the start/ end logs. Something for sequence of games as well
[ ] Track who is playing to get stats on each agent. 
[ ] log force quit
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
    startingPlayer: Mapped[int] # 1 for blue, 2 for red
    # end game optional stuff
    winner: Mapped[Optional[int]] # 1 for blue, 2 for red, None for unfinished game
    endSequence: Mapped[Optional[int]] # The total number of moves in the finished game

    moves: Mapped[List["Move"]] = relationship(
        back_populates="game", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Game(id={self.id!r}, blueAgent={self.blueAgent!r}, redAgent={self.redAgent!r}, startingPlayer={self.startingPlayer!r}, winner={self.winner!r}, endSequence={self.endSequence!r})"

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

# COMEBACK this guy will need their own file
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


    def logStartGame(self, blueAgent: str, redAgent: str, startingPlayer: int) -> None:
        """"""
        currentGame = Game(
            blueAgent = blueAgent,
            redAgent = redAgent,
            startingPlayer = startingPlayer
        )
        self.gameSequence = -1 # IDK if this should be inside here. start at -1 so the first move is 0
        self.gameInProgress = True

        with Session(self.engine) as session:
            session.add(currentGame)
            session.commit()
            self.currentGameId = currentGame.id

    def logMove(self, player: int, move: Hex) -> None:

        if (not self.gameInProgress):
            return # COMEBACK do I want this? I might want this to fail or say something 

        with Session(self.engine) as session: 
            self.gameSequence += 1
            m = Move(player, move, self.gameSequence)
            query = (
                select(Game)
                .where(Game.id == self.currentGameId)
            )
            currentGame = session.scalars(query).one()
            currentGame.moves.append(m)
            session.commit()

    def logEndGame(self, winnerId: int) -> None:
        self.gameInProgress = False

        with Session(self.engine) as session:

            query = (
                select(Game)
                .where(Game.id == self.currentGameId)
            )

            g = session.scalars(query).one()
            g.winner = winnerId
            g.endSequence = self.gameSequence

            session.commit()

    def printGameSequence(self) -> None:
        print()
        with Session(self.engine) as session:
            query = (
                select(Move)
                .where(Move.game_id == self.currentGameId)
            )

            for m in session.scalars(query):
                print(m)

            query = (
                select(Game)
                .where(Game.id == self.currentGameId)
            )

            g = session.scalars(query).one()
            print(g)
        print()

    def getMovesForGameId(self, gameId: int) -> List[tuple]:
        moves: List[tuple] = []
        with Session(self.engine) as session:
            query = (
                select(Move)
                .where(Move.game_id == gameId)
                .order_by(asc(Move.sequence))
            )

            for m in session.scalars(query):
                moves.append((m.player, (m.x, m.y)))

        return moves
            


            

def initDB() -> None:
    xLogger = HexLogger()

    uhh = xLogger.getMovesForGameId(4)
    print(uhh)

def resetDatabase() -> None:
    """This creates the tables for the logger and refreshes the database probably"""
    xLogger = HexLogger()
    xLogger.resetDB()
    xLogger.initDBTables()


    # TODO need some sort of confirmation to prevent accidental resets
    print("Database reset")


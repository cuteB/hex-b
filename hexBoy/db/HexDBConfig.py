from hexBoy.hex.node.HexNode import Hex
from typing import List, Optional
from sqlalchemy import create_engine, ForeignKey, Engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

'''
[ ] I think I want to add the time to the logs
[x] create logger interface so I can swap out the DB later
[ ] A GameHistory table that tracks the start/ end logs. Something for sequence of games as well
[ ] Track who is playing to get stats on each agent. 
[ ] log force quit, other user actions as well
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
    gameType: Mapped[str] # mostly to check if the game is a test game
    gameNote: Mapped[str] # Additional notes on the game if needed. Probably for testing

    moves: Mapped[List["Move"]] = relationship(
        back_populates="game", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Game(id={self.id!r}, blueAgent={self.blueAgent!r}, redAgent={self.redAgent!r}, startingPlayer={self.startingPlayer!r}, winner={self.winner!r}, endSequence={self.endSequence!r}, gameType={self.gameType!r}, gameNote={self.gameNote!r})"

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

'''---
DB Connection Strings
---'''
class HexDBConfig:
    connectionPath = 'hexBoy/db/hex_sqlite.db' 
    connectionString = 'sqlite:///' + connectionPath
    
'''---
Logger Event Interface
---'''
class EventType: # COMEBACK I don't like this name
    START_GAME = "start_game"
    MOVE = "move"
    END_GAME = "end_game"

'''---
HexDBManager
---'''
class HexDBManager:  
    connectionString = HexDBConfig.connectionString
    engine: Engine


    def __init__(self):
        self.engine = create_engine(self.connectionString)

    def resetDB(self):
        print("Dropping DB Tables")
        Game.__table__.drop(self.engine)
        Move.__table__.drop(self.engine)

    def initDBTables(self) -> None:
        print("Creating DB Tables")
        Base.metadata.create_all(self.engine)

'''---
Database Setup Functions
---'''
def initDB() -> None:
    """Create the actual database and initialize the tables"""
    xLogger = HexDBManager()
    xLogger.initDBTables()
    print("Database initialized")
    
def resetDatabase() -> None:
    """This creates the tables for the logger and refreshes the database probably"""

    # Confirm
    confirmation = input("Are you sure you want to reset the database? (y/n): ")

    if (confirmation == "y"):
        print("Resetting database")
        xLogger = HexDBManager()
        xLogger.resetDB()
        xLogger.initDBTables()
        print("Database reset Complete")

    else:
        print("Database reset aborted")

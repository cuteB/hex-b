# TODO probably rename this file and create a setup file that is separate from the logger
import threading
import queue
import time

from abc import ABC, abstractmethod

from hexBoy.hex.node.HexNode import Hex
from typing import List, Optional
from sqlalchemy import create_engine, ForeignKey, String, select, Engine, asc
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

'''
[ ] I think I want to add the time to the logs
[ ] create logger interface so I can swap out the DB later
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




# HACK 
class LoggerSink(queue.Queue):
    def __init__(self):
        super().__init__(maxsize=1000) # not 1000 but idk maybe that many. how many logs is too many

    def getMessage(self):
        value = self.get()
        return value
    
    def setMessage(self, value):
        self.put(value)
# HACK


'''---
BaseLogger
---'''
class BaseLogger(ABC):
    """Base class for logging events to a database"""

    @abstractmethod
    def logEvent(self, event: str, obj: any) -> None:
        """Log an event to the database"""

    @abstractmethod
    def loggerThread(self, event: threading.Event) -> None:
        """Thread to log events to the database"""
    


# Enums for the types of events
class EventType: # COMEBACK I don't like this name
    START_GAME = "start_game"
    MOVE = "move"
    END_GAME = "end_game"

'''---
HexLogger
---'''
# COMEBACK this guy will need their own file
class HexLogger:  
    connectionPath = 'hexBoy/db/hex_sqlite.db' # TODO there is some garbage tables still in here
    connectionString = 'sqlite:///' + connectionPath
    engine: Engine

    _lock = threading.Lock()

    currentGame: Game
    currentGameId: int
    gameSequence: int
    gameInProgress: bool # COMEBACK I might want to merge this with the currentGameId to track if a game is in progress

    _LoggerSink: LoggerSink # I like sink better

    '''
    [ ] I want to be able to configure if I want to use the logger or not. Maybe just a flag that I can set in the config
        In addition I think it would be cool for the logger to know if there isn't a database setup and then give a warning.
        Maybe just use the mock logger but I would be mad if I ran tons of games and then realized I didn't have the logger on
    [ ] Set config flag in main.py to use mock logger.
    [ ] Setup threads for the logger so that the w/r doesn't take time out of the agents. The logger should be its own thread and
        the agents/game should put the events they want to log into a sink (maybe sync idk but thats what they say at work)
    [ ] Probs want to setup some logging class that handles the threading.
    '''

    def __init__(self):
        self.engine = create_engine(self.connectionString)
        self.gameInProgress = False

        self._loggerSink = LoggerSink()


    # Enums for the types of events
    class EventType:
        START_GAME = "start_game"
        MOVE = "move"
        END_GAME = "end_game"

    def logEvent(self, event: EventType, obj: any) -> None:
        """Log an event to the database"""
        self._loggerSink.setMessage((event, obj))


    '''---
    Logging Thread
    ---'''
    def _loggerThread(self, event) -> None:
        """Thread to log events to the database"""

        while not event.is_set() or self._loggerSink.qsize() != 0: # Run until game over and queue is finished
            if self._loggerSink.qsize() != 0:
                # Log event in the database
                message = self._loggerSink.getMessage()

                if message[0] == EventType.START_GAME:
                    self._logStartGame(*message[1])

                elif message[0] == EventType.MOVE:
                    self._logMove(*message[1])

                elif message[0] == EventType.END_GAME:
                    self._logEndGame(*message[1])
                
            else: # sleep for a bit if no logs in queue
                time.sleep(0.1) 

        print("\nLogger done") # XXX


    def xSet(self, log):
        # TODO need this for mock if using this but I'll probably deal with that in a better way within each log function
        
        print("\nset", log) # XXX
        self._loggerSink.setMessage(log)

    # def xGet(self): # I don't think this is used

    #     uhh =  self._loggerSink.getMessage()
    #     return uhh




    


    '''---
    Database config
    ---'''
    # COMEBACK I may put this in another class to separate this from the actual telemetry logging

    def resetDB(self):
        Game.__table__.drop(self.engine)
        Move.__table__.drop(self.engine)

    def initDBTables(self) -> None:
        Base.metadata.create_all(self.engine)

    '''---
    Actual logging methods
    ---'''
    def _logStartGame(self, blueAgent: str, redAgent: str, startingPlayer: int, gameType: str = "", gameNote: str = "") -> None:
        """Log the start of a game"""
        
        currentGame = Game(
            blueAgent = blueAgent,
            redAgent = redAgent,
            startingPlayer = startingPlayer,
            gameType = gameType,
            gameNote = gameNote
        )
        self.gameSequence = -1 # IDK if this should be inside here. start at -1 so the first move is 0
        self.gameInProgress = True

        with Session(self.engine) as session:
            session.add(currentGame)
            session.commit()
            self.currentGameId = currentGame.id



    def _logMove(self, player: int, move: Hex) -> None:
        """Log move from a game"""

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

    def _logEndGame(self, winnerId: int) -> None:
        """Log the end of a game"""
        def _logEndGame(winnerId: int) -> None:
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

        # Start thread to log
        with self._lock:
            x = threading.Thread(target=_logEndGame, args=(winnerId,))
            x.start()




    '''---
    Query methods
    ---'''
    # COMEBACK just like the database management functions this should probably be in a HexQuery class
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
    
        
            

# '''---
# Logger Sink
# ---'''
# # > Is it Sync or Sink. 

# class LoggerSink(queue.Queue):

#     def __init__(self):
#         super().__init__(maxsize=10) # idk if this needs to be bigger than 10 but I think it has to be set to something

#     def addLog(self, logType: str, kwargs) -> None:

#         _obj = {logType, kwargs}
#         self.put(_obj)


#     def getLog(self):

#         logType, kwargs = self.get()

#         print(logType, *kwargs)            


'''---
Mock Logger
---'''
class MockLogger(BaseLogger):
    """Mock logger that does nothing with events"""
    
    def logEvent(self, event: str, obj: any) -> None:
        """Log an event to the database"""
        pass

    def loggerThread(self, event: threading.Event) -> None:
        """Thread to log events to the database"""
        pass




# [ ] Move these to a place within the database class and title these as setup functions
# [ ] Add some additional console logs to show how cool my setup is
def initDB() -> None:
    """Create the actual database and initialize the tables"""
    xLogger = HexLogger()
    xLogger.initDBTables()
    print("Database initialized")
    
def resetDatabase() -> None:
    """This creates the tables for the logger and refreshes the database probably"""
    xLogger = HexLogger()
    xLogger.resetDB()
    xLogger.initDBTables()


    # TODO need some sort of confirmation to prevent accidental resets
    print("Database reset")


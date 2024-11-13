import threading
import queue
import time

from abc import ABC, abstractmethod
from sqlalchemy import create_engine, select, Engine
from sqlalchemy.orm import  Session

from hexBoy.db.HexDBConfig import HexDBConfig, Game, Move
from hexBoy.hex.node.HexNode import Hex


class LoggerSink(queue.Queue):
    def __init__(self):
        super().__init__(maxsize=1000) # not 1000 but idk maybe that many. how many logs is too many

    def getMessage(self):
        value = self.get()
        return value
    
    def setMessage(self, value):
        self.put(value)

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
class HexLogger:  
    connectionString = HexDBConfig.connectionString
    engine: Engine

    _lock = threading.Lock()

    currentGame: Game
    currentGameId: int
    gameSequence: int
    gameInProgress: bool # COMEBACK I might want to merge this with the currentGameId to track if a game is in progress

    _LoggerSink: LoggerSink # I like sink better

    '''
    [x] I want to be able to configure if I want to use the logger or not. Maybe just a flag that I can set in the config
        In addition I think it would be cool for the logger to know if there isn't a database setup and then give a warning.
        Maybe just use the mock logger but I would be mad if I ran tons of games and then realized I didn't have the logger on
    [x] Set config flag in main.py to use mock logger.
    [x] Setup threads for the logger so that the w/r doesn't take time out of the agents. The logger should be its own thread and
        the agents/game should put the events they want to log into a sink (maybe sync idk but thats what they say at work)
    [x] Probs want to setup some logging class that handles the threading.
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
    def loggerThread(self, event) -> None:
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

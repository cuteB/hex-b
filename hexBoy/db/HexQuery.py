# TODO probably rename this file and create a setup file that is separate from the logger

from typing import List
from sqlalchemy import  select, Engine, asc
from sqlalchemy.orm import  Session

from hexBoy.db.HexDBConfig import HexDBConfig, Game, Move

'''---
HexQuery class
---'''
# COMEBACK this guy will need their own file
class HexQuery:  
    connectionString = HexDBConfig.connectionString
    engine: Engine

    '''---
    Query methods
    ---'''
    def printGameSequence(self) -> None:
        """Print the current game sequence"""
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
    
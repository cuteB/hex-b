from sqlalchemy import select
from sqlalchemy.orm import Session
from hexBoy.db.HexDBConfig import  Game, Move
from hexBoy.db.HexQuery import  HexQuery

def listMovesForGame(param: str) -> None:
    """List all of the moves for a given game."""
    gameId = int(param)

    xQ = HexQuery()
    with Session(xQ.engine) as session:
        query = (
            select(Move)
            .where(Move.game_id == gameId)
        )

        for m in session.scalars(query):
            print(m)
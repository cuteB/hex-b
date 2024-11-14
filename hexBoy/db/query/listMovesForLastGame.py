from sqlalchemy import select, func
from sqlalchemy.orm import Session
from hexBoy.db.HexDBConfig import  Game, Move
from hexBoy.db.HexQuery import  HexQuery

def listMovesForLastGame() -> None:
    """List all of the  moves for the last game played."""

    # Print out the list of all of the games
    xQ = HexQuery()
    with Session(xQ.engine) as session:
        query = (
            func.max(Game.id)
        )

        # get the max game id
        gameId = session.scalar(query)

        query = (
            select(Move)
            .where(Move.game_id == gameId)
        )

        for m in session.scalars(query):
            print(m)

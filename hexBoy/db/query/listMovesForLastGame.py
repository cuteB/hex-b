from sqlalchemy import select, func
from sqlalchemy.orm import Session
from hexBoy.db.logger.HexDBSetup import HexLogger, Game, Move

def listMovesForLastGame() -> None:
    """List all of the  moves for the last game played."""

    # Print out the list of all of the games
    xLogger = HexLogger()
    with Session(xLogger.engine) as session:
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
from sqlalchemy import select
from sqlalchemy.orm import Session
from hexBoy.db.logger.HexDBSetup import HexLogger, Game, Move

def listMovesForGame(param: str) -> None:
    """List all of the moves for a given game."""
    gameId = int(param)

    xLogger = HexLogger()
    with Session(xLogger.engine) as session:
        query = (
            select(Move)
            .where(Move.game_id == gameId)
        )

        for m in session.scalars(query):
            print(m)
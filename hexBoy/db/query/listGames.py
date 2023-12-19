from sqlalchemy import select
from sqlalchemy.orm import Session
from hexBoy.db.logger.HexDBSetup import HexLogger, Game

def listGames(param: str) -> None:
    # Print out the list of all of the games
    xLogger = HexLogger()
    with Session(xLogger.engine) as session:
        query = (
            select(Game)
        )

        for g in session.scalars(query):
            print(g)
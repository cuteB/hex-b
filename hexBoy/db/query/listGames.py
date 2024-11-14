from sqlalchemy import select
from sqlalchemy.orm import Session
from hexBoy.db.HexDBConfig import  Game
from hexBoy.db.HexQuery import  HexQuery

def listGames() -> None:
    # Print out the list of all of the games
    xQ = HexQuery()
    with Session(xQ.engine) as session:
        query = (
            select(Game)
        )

        for g in session.scalars(query):
            print(g)

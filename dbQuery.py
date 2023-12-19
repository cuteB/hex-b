import sys
from hexBoy.db.logger.HexDBSetup import resetDatabase
from hexBoy.db.query.listGames import listGames
from hexBoy.db.query.listMovesForGame import listMovesForGame

def main():

    inputs = [opt for opt in sys.argv[1:]]

    if (len(inputs) not in (1,2)):
        print("Invalid query. Only one argument allowed. type 'help' for the list of queries")
        return
    
    print()
    
    if (len(inputs) == 1):
        param = ""
    else:
        param = inputs[1]
    
    query = inputs[0]

    if (query=="help"):
        plsHelp()

    if (query == "resetDatabase_DANGER"):
        resetDatabase()

    if (query == "listGames"):
        listGames(param)

    if (query == "listMovesForGame"):
        listMovesForGame(param)

    

def plsHelp():
    """Print out the list of queries I have"""
    print("listGames\t\t\tList all of the games in the db")
    print("listMovesForGame <gameId> \tList all of the moves for a single game")    


if __name__ == "__main__":
    main()

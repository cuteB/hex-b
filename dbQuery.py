import sys
from hexBoy.db.logger.HexDBSetup import initDB, resetDatabase
from hexBoy.db.query.listGames import listGames

def main():

    inputs = [opt for opt in sys.argv[1:]]

    if (len(inputs) not in (1,2)):
        print("Invalid query. Only one argument allowed.")
        return
    
    if (len(inputs) == 1):
        param = ""
    else:
        param = inputs[1]
    
    query = inputs[0]
    print(query)

    if (query == "resetDatabase_DANGER"):
        resetDatabase()

    if (query == "listGames"):
        print("uhh")
        listGames(param)
    

    





if __name__ == "__main__":
    main()

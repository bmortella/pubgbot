import operator
from tinydb import TinyDB, Query
from game_model import Game
from player_model import Player

class Database:

    def __init__(self, debug=False):
        self.__connection = TinyDB('data.json')
        self.__debug = debug
        if debug:
            print("Conexão estabelecida com a db")

    def __add_players(self, players):
        players_table = self.__connection.table('players')
        for id, kills in players.items():
            player = players_table.get(Query().id == id)
            if player:
                kills += player['kills']
            players_table.upsert({'id':id, 'kills':kills}, Query().id == id)

    def add_win(self, data):
        games_table = self.__connection.table('games')
        games_table.insert(data)
        self.__add_players(data['players'])

    #Return an ordered list (by total kills) of wins
    @property
    def wins(self):
        games_table = self.__connection.table('games')
        games_list = list()
        for row in games_table.all():
            games_list.append(Game(row['players'], row['total']))
        return sorted(games_list, key=operator.attrgetter('total'), reverse=True)

    @property
    def players(self):
        players_table = self.__connection.table('players')
        players_list = list()
        for row in players_table.all():
            players_list.append(Player(row['id'], row['kills']))
        return sorted(players_list, key=operator.attrgetter('kills'), reverse=True)


#Test
if __name__ == "__main__":
    db = TinyDB('data.json')
    players = db.table('players')
    games = db.table('games')

    print(games.all())
    print(players.all())    



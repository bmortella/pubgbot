import peewee
from models import Player, Winner, Win

class Manager:

    __win_type = {0:"kills", 1:"solo", 2:"duo", 4:"squad"}

    def __init__(self):
        db = peewee.SqliteDatabase("data.db")
        try:
            db.create_tables([Player, Win, Winner])
            print("Tabelas criadas no banco.")
        except peewee.OperationalError:
            print("{} jogadores carregados.".format(Player.select().count()))
            print("{} vitórias carregadas.".format(Win.select().count()))


    def add_win(self, data, win_type):
        win = Win.create()
        total_kills = 0
        for discord_id, kills in data.items():
            player, created = Player.get_or_create(discord_id=discord_id)
            exec('player.total_{} += {}'.format(self.__win_type[win_type], kills))
            player.total_kills += kills
            player.save()

            Winner.create(win=win, player=player, kills=kills)
            total_kills += kills
        win.total_kills = total_kills
        win.win_type = win_type
        win.save()
        

    def rank_players(self, win_type):
        if win_type == 0:
            total = Player.select().where(Player.total_kills != 0).count()
            obj_list = Player.select().order_by(Player.total_kills.desc()).limit(5)
        elif  win_type == 1:
            total = Player.select().where(Player.total_solo != 0).count()
            obj_list = Player.select().order_by(Player.total_solo.desc()).limit(5)
        elif win_type == 2:
            total = Player.select().where(Player.total_duo != 0).count()
            obj_list = Player.select().order_by(Player.total_duo.desc()).limit(5)
        else:
            total = Player.select().where(Player.total_squad != 0).count()
            obj_list = Player.select().order_by(Player.total_squad.desc()).limit(5)
        return (obj_list, total)

    def rank_wins(self, win_type)
        total = Win.select().where(Win.win_type == win_type).count()
        obj_list = Win.select().where(Win.win_type == win_type).order_by(obj.total_kills.desc()).limit(5)
        return (obj_list, total)
import peewee
from models import Player, Winner, Win

class Manager:

    def __init__(self):
        db = peewee.SqliteDatabase("data.db")
        try:
            db.create_tables([Player, Win, Winner])
            print("Tabelas criadas no banco.")
        except peewee.OperationalError:
            print("{} jogadores carregados.".format(Player.select().count()))
            print("{} vitórias carregadas.".format(Win.select().count()))


    def add_win(self, data):
        win = Win.create()
        total_kills = 0
        for discord_id, kills in data.items():
            player, created = Player.get_or_create(discord_id=discord_id)
            player.total_kills += kills
            player.save()

            Winner.create(win=win, player=player, kills=kills)
            total_kills += kills
        win.total_kills = total_kills
        win.save()
        

    def rank(self, obj):
        total = obj.select().count()
        obj_list = (obj.select().order_by(obj.total_kills.desc()).limit(5))
        return (obj_list, total)
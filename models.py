import peewee, datetime
from playhouse.fields import ManyToManyField

db = peewee.SqliteDatabase('data.db')

class BaseModel(peewee.Model):
    class Meta:
        database = db

class Player(BaseModel):

    discord_id = peewee.CharField(unique=True)
    total_kills = peewee.IntegerField(default=0)


class Win(BaseModel):
 
    date = peewee.DateTimeField(default=datetime.datetime.now)
    total_kills = peewee.IntegerField(default=0)

class Winner(BaseModel):

    win = peewee.ForeignKeyField(Win, related_name="winners", null=False)
    player = peewee.ForeignKeyField(Player, related_name="wins")
    kills = peewee.IntegerField()


if __name__ == '__main__':
    try:
        db.create_tables([Player, Win, Winner])
    except Exception:
        pass
    ###
    pla = Player.create(discord_id="656565", total_kills=2)
    win = Win.create()
    winp = Winner.create(win=win, player=pla, kills=2)
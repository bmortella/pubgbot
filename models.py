import peewee, datetime
from playhouse.fields import ManyToManyField

db = peewee.SqliteDatabase('data.db')

class BaseModel(peewee.Model):
    class Meta:
        database = db

class Player(BaseModel):

    discord_id = peewee.CharField(unique=True)
    total_solo = peewee.IntegerField(default=0)
    total_duo = peewee.IntegerField(default=0)
    total_squad = peewee.IntegerField(default=0)
    total_kills = peewee.IntegerField(default=0)

'''
win_type
1 = solo
2 = duo
4 = squad
'''
class Win(BaseModel):
 
    date = peewee.DateTimeField(default=datetime.datetime.now)
    total_kills = peewee.IntegerField(default=0)
    win_type = peewee.IntegerField(default=4)

class Winner(BaseModel):

    win = peewee.ForeignKeyField(Win, related_name="winners", null=False)
    player = peewee.ForeignKeyField(Player, related_name="wins")
    kills = peewee.IntegerField()


if __name__ == '__main__':
    '''
    pla = Player.select().order_by(Player.total_kills.desc()).get()
    print(pla)
    '''
    
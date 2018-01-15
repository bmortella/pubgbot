import discord
from discord.ext import commands
from models import Player, Win
from manager import Manager
import config


class CommandException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


win_types = {"geral":0, "solo":1, "duo":2, "squad":4}

bot = commands.Bot(command_prefix=config.PREFIX, description='A bot to keep track of our wins and kills')
db = Manager()

@bot.event
async def on_ready():
    await bot.change_presence(game=discord.Game(name="PLAYERUNKNOWN'S BATTLEGROUNDS"))
    print ('Pronto!')


@bot.command(pass_context=True)
async def winner(context, *args : str):
    len_args = len(args)
    if len_args == 1:
        try:
            kills = int(args[0])
            data = {context.message.author.mention:kills}
            db.add_win(data, 1)
            await bot.say("Registrado.")
        except ValueError:
            pass
    elif len_args % 2 == 0:
        try:
            nplayers = len_args / 2
            if nplayers >= 2 and nplayers <= 4:
                data = dict()
                for i in range(0, len(args), 2):
                    player = args[i]
                    if not player.startswith("<"):
                        raise CommandException("Menção feita de forma errada: {}".format(player))
                    try:
                        kills = int(args[i+1])
                    except ValueError:
                        raise CommandException("Erro, {} não é um número.".format(args[i+1]))
                    data[player] = kills
                win_type = nplayers if nplayers != 3 else 4
                db.add_win(data, win_type)
                await bot.say("Registrado.")
            else:
                raise CommandException("{}, registre apenas wins com no máximo 4 jogadores.".format(context.message.author.mention))
        except CommandException as e:
            await bot.say(e.value)
    else:
        await bot.say("{}, número errado de parâmetros.".format(context.message.author.mention))


@bot.group(pass_context=True)
async def rank(ctx):
    if ctx.invoked_subcommand is None:
        await bot.say('Comando inválido..')

@rank.command()
async def wins(win_type:str="squad"):
    try:
        win_type = win_type.lower()
        if win_type not in win_types:
            raise CommandException("Erro, apenas solo, duo ou squad")
        else:
            if win_type == "geral": win_type = "squad"
        wins, wins_total = db.rank_wins(win_types[win_type])
        if wins_total > 0:
            embed = discord.Embed(
                title="Rank de vitórias em {}".format(win_type),
                color=0xe67e22  
            )
            r = 1
            for win in wins:
                winners = str()
                for winner in win.winners:
                    winners += "{} : {} kills\n".format(winner.player.discord_id, winner.kills)
                embed.add_field(
                        name="{}°".format(r),
                        value=winners+"\nTotal: {}\nData: {}".format(win.total_kills, win.date.strftime("%d/%m/%y %H:%M")),
                        inline=False
                    )
                r += 1
            embed.set_footer(
                text="Total de partidas: {}".format(wins_total)
            )
            await bot.say(embed=embed)
        else:
            await bot.say("Ainda não há vitórias.")
    except CommandException as e:
        await bot.say(e.value)

@rank.command()
async def jogadores(win_type:str="squad"):
    try:
        win_type = win_type.lower()
        if win_type not in win_types:
            raise CommandException("Erro, apenas geral, solo, duo ou squad")
        players, total = db.rank_players(win_types[win_type])
        if total > 0:
            embed = discord.Embed(
                title="Rank de jogadores em {}".format(win_type),
                color=0xe67e22
            )
            r = 1
            for player in players:
                discord_id = player.discord_id
                kills = player.total_kills
                embed.add_field(
                    name="{}°".format(r),
                    value="{} : {} kills\n".format(discord_id, kills),
                    inline=False
                )
                r += 1
            embed.set_footer(
                text="Total de jogadores: {}".format(total)
            )
            await bot.say(embed=embed)
        else:
            await bot.say("Ainda não há jogadores.")
    except CommandException as e:
        await bot.say(e.value)

@bot.command()
async def fechar():
    await bot.say("Saindo...")
    bot.close()
    exit()


bot.pm_help = True
bot.run(config.TOKEN)
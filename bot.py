import discord
from discord.ext import commands
from manager import Manager
import config

bot = commands.Bot(command_prefix=config.PREFIX, description='A bot to keep track of our wins and kills')
db = Manager()

@bot.event
async def on_ready():
    await bot.change_presence(game=discord.Game(name="PLAYERUNKNOWN'S BATTLEGROUNDS"))
    print ('Pronto!')


@bot.command(pass_context=True)
async def winner(context, *args : str):
    len_args = len(args)
    if len_args % 2 == 0:
        if len_args / 2 >= 3:
            data = dict()
            do = True
            i = 0
            while i < len(args) and do:
                player = args[i]
                if not player.startswith("<"):
                    await bot.say("Menção feita de forma errada: {}".format(player))
                    do = False
                    break
                try:
                    kills = int(args[i+1])
                except ValueError:
                    do = False
                    await bot.say("Erro, {} não é um número.".format(args[i+1]))
                data[player] = kills
                i += 2
            if do:
                db.add_win(data)
                await bot.say("Registrado.")
        else:
            await bot.say("{}, registre apenas wins com 3 ou mais jogadores.".format(context.message.author.mention))
    else:
        await bot.say("{}, número errado de parâmetros.".format(context.message.author.mention))


@bot.group(pass_context=True)
async def rank(ctx):
    if ctx.invoked_subcommand is None:
        await bot.say('Comando inválido..')

@rank.command()
async def wins():
    wins, wins_total = db.rank_wins()
    if wins_total > 0:
        embed = discord.Embed(
            title="Rank de vitórias",
            color=0xe67e22  
        )
        r = 1
        for win in wins:
            winners = str()
            for winner in win.winners:
                winners += "{} : {} kills\n".format(winner.player.discord_id, winner.kills)
            embed.add_field(
                    name="{}°".format(r),
                    value=winners,
                    inline=False
                )
            r += 1
        embed.set_footer(
            text="Total de partidas: {}".format(wins_total)
        )
        await bot.say(embed=embed)
    else:
        await bot.say("Ainda não há vitórias.")

@rank.command()
async def jogadores():
    players_list = db.players
    embed = discord.Embed(
        title="Rank de jogadores",
        color=0xe67e22
    )
    for i in range(5):
        id = players_list[i].id
        kills = players_list[i].kills
        player = "{} : {} kills\n".format(id, kills)
        embed.add_field(
            name="{}°".format(i + 1),
            value=player,
            inline=False
        )
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def teste(ctx):
    await bot.send_message(ctx.message.channel, ctx.message.author)
    await bot.send_message(ctx.message.channel, ctx.message.content)
    print(ctx.message.author.id)
    print (ctx.message.content)


bot.pm_help = True
bot.run(config.TOKEN)
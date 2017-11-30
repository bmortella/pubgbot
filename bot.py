import discord
from discord.ext import commands
from database import Database
import config

bot = commands.Bot(command_prefix=config.PREFIX, description='A bot to keep track of our wins and kills')
db = Database(debug=True)

@bot.event
async def on_ready():
    await bot.change_presence(game=discord.Game(name="PLAYERUNKNOWN'S BATTLEGROUNDS"))
    print ('Pronto!')


@bot.command(pass_context=True)
async def winner(context, *args : str):
    if len(args) % 2 == 0:
        players_dict = dict()
        total = 0
        for i in range(0, len(args), 2):
            kills = int(args[i+1])
            players_dict[args[i]] = kills
            total += kills
        data = {'players':players_dict, 'total':total}
        db.add_win(data)
        await bot.say("Registrado")
    else:
        await bot.say("{}, há algo de errado com os parâmetros.".format(context.author.mention))


@bot.group(pass_context=True)
async def rank(ctx):
    if ctx.invoked_subcommand is None:
        await bot.say('Comando inválido..')

@rank.command()
async def wins():
    games_list = db.wins
    embed = discord.Embed(
        title="Rank de vitórias",
        color=0xe67e22  
    )
    for win in range(5):
        winners = str()
        for key, value in games_list[win].winners.items():
            winners += "{} : {} kills\n".format(key, value)
        embed.add_field(
                name="{}°".format(win + 1),
                value=winners,
                inline=False
            )
    embed.set_footer(
        text="Total de partidas: {}".format(len(games_list))
    )
    await bot.say(embed=embed)

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
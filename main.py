import discord
import os
from dotenv import load_dotenv
import wavelink

load_dotenv()
bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    await connect_nodes()  # connect to the server

async def connect_nodes():
    """Connect to our Lavalink nodes."""
    await bot.wait_until_ready()  # wait until the bot is ready

    await wavelink.NodePool.create_node(
        bot=bot,
        host='127.0.0.1',
        port=2333,
        password=os.getenv("LAVALINK_PASSWORD")
    )  # create a node

@bot.event
async def on_wavelink_node_ready(node: wavelink.Node):
    print(f"{node.identifier} is ready.")  # print a message


@bot.slash_command()
async def 안녕(ctx):
    await ctx.respond("안녕하세요!")


for cog in os.listdir("cogs"):
    if cog.endswith('.py'):
        bot.load_extension(f"cogs.{cog[:-3]}")


bot.run(os.getenv("TOKEN"))

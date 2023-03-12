import discord
import os
from dotenv import load_dotenv
import wavelink

load_dotenv()
intents = discord.Intents.all()
bot = discord.Bot(intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user}")
    await connect_nodes()

async def connect_nodes():
    await bot.wait_until_ready()

    await wavelink.NodePool.create_node(
        bot=bot,
        host='127.0.0.1',
        port=2333,
        password=os.getenv("LAVALINK_PASSWORD")
    )

@bot.event
async def on_wavelink_node_ready(node: wavelink.Node):
    print(f"{node.identifier} is ready.")


@bot.slash_command()
async def 안녕(ctx):
    await ctx.respond("안녕하세요!")


for cog in os.listdir("cogs"):
    if cog.endswith('.py'):
        bot.load_extension(f"cogs.{cog[:-3]}")

bot.run(os.getenv("TOKEN"))

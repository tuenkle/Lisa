import discord
import os
from dotenv import load_dotenv

load_dotenv()
bot = discord.Bot()

@bot.slash_command()
async def hello(ctx):
    await ctx.respond("Hello!")

for cog in os.listdir("cogs"):
    bot.load_extension(f"cogs.{cog[:-3]}")

bot.run(os.getenv("TOKEN"))


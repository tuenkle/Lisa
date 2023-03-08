import discord
from discord.ext import commands
import wavelink

class Music(commands.Cog):  # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot):  # this is a special method that is called when the cog is loaded
        self.bot = bot

    @discord.slash_command(name="stop", description="stop song")
    async def stop(self, ctx):
        vc = ctx.voice_client

        if not vc:
            return await ctx.respond("Currently not playing song.")

        await vc.disconnect()
        await ctx.respond("End playing the song.")

    @discord.slash_command(name="play", description="play song")
    async def play(self, ctx, search: str):
        vc = ctx.voice_client  # define our voice client

        if not vc:  # check if the bot is not in a voice channel
            vc = await ctx.author.voice.channel.connect(cls=wavelink.Player)  # connect to the voice channel
        if ctx.author.voice is None:
            return await ctx.respond("You must be in the voice channel.")
        if ctx.author.voice.channel.id != vc.channel.id:  # check if the bot is not in the voice channel
            return await ctx.respond("You must be in the same voice channel as the bot.")  # return an error message
        song = await wavelink.YouTubeTrack.search(query=search, return_first=True)  # search for the song

        if not song:  # check if the song is not found
            return await ctx.respond("No song found.")  # return an error message

        await vc.play(song)  # play the song
        await ctx.respond(f"Now playing: `{vc.source.title}`")  # return a message

def setup(bot):
    bot.add_cog(Music(bot))
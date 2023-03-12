import discord
from discord.ext import commands
import wavelink

class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="노래를 중지합니다.")
    async def 중지(self, ctx):
        vc = ctx.voice_client

        if not vc:
            return await ctx.respond("Currently not playing song.")

        await vc.disconnect()
        await ctx.respond("End playing the song.")

    @discord.slash_command(description="노래를 재생합니다.")
    async def 재생(self, ctx, search: str):
        vc = ctx.voice_client

        if not vc:
            vc = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        if ctx.author.voice is None:
            return await ctx.respond("You must be in the voice channel.")
        if ctx.author.voice.channel.id != vc.channel.id:
            return await ctx.respond("You must be in the same voice channel as the bot.")
        song = await wavelink.YouTubeTrack.search(query=search, return_first=True)

        if not song:  # check if the song is not found
            return await ctx.respond("No song found.")

        await vc.play(song)  # play the song
        await ctx.respond(f"Now playing: `{vc.source.title}`") 

def setup(bot):
    bot.add_cog(Music(bot))
import discord
from discord.ext import commands
import utils
import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin
import os
from datetime import datetime
class Drawing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @discord.slash_command(description="긍정프롬에는 원하는 내용을, 부정프롬에는 지양하는 내용을 적어주세요.")
    async def 그림(self, ctx, 긍정프롬: discord.Option(str) = "", 부정프롬: discord.Option(str) = ""):
        await ctx.respond("그림을 그리는 중...")
        if utils.contains_hangul(긍정프롬):
            긍정프롬 = utils.translate(긍정프롬)
            if 긍정프롬.startswith("Error Code:"):
                await ctx.respond("오류가 발생했습니다.")
                return
        if utils.contains_hangul(부정프롬):
            부정프롬 = utils.translate(부정프롬)
            if 부정프롬.startswith("Error Code:"):
                await ctx.respond("오류가 발생했습니다.")
                return
        print(긍정프롬)
        print(부정프롬)
        url = os.getenv("DRAWING_API_IP")
        payload = {
            "denoising_strength": 0.5,
            "prompt": 긍정프롬,
            "seed": -1,
            "batch_size": 1,
            "steps": 25,
            "cfg_scale": 7,
            "width": 786,
            "height": 786,
            "negative_prompt": f"NSFW, {부정프롬}",
            "sampler_index": "Euler a",
        }

        response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
        print(response)
        r = response.json()

        for i in r['images']:
            image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))

            png_payload = {
                "image": "data:image/png;base64," + i
            }
            response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

            pnginfo = PngImagePlugin.PngInfo()
            pnginfo.add_text("parameters", response2.json().get("info"))
            image.save('output.png', pnginfo=pnginfo)
        file = discord.File("output.png", filename="output.png")
        embed = discord.Embed(title=f"그림 생성 완료 at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                              description=f"by {ctx.author}")
        embed.set_image(url="attachment://output.png")
        embed.add_field(name="긍정 프롬프트", value=긍정프롬, inline=False)
        embed.add_field(name="부정 프롬프트", value=부정프롬, inline=True)
        await ctx.respond(file=file, embed=embed)

def setup(bot):
    bot.add_cog(Drawing(bot))
import discord
from discord.ext import commands
import utils
import os
import openai
class Chatbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        openai.api_key = os.getenv("OPENAI_API_KEY")
        Chatbot.previous = ""
        Chatbot.currently_working = False
    @discord.slash_command()
    async def 챗(self, ctx, arg: str):
        Chatbot.currently_working = True
        await ctx.respond("채팅을 작성하는 중...")
        model = "gpt-3.5-turbo"
        if Chatbot.previous == "":
            messages = [
                {"role": "user", "content": arg}
            ]
            Chatbot.previous += f"{ctx.author}: {arg}"
        else:
            token_count = utils.num_tokens_from_messages([{"role": "system", "content": Chatbot.previous}])
            print(token_count)
            if token_count > 2000:
                messages = [
                    {"role": "user", "content": f"다음 대화를 2000자 이내로 자세하게 설명해줘. {Chatbot.previous}"}
                ]
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=messages
                )
                answer = response['choices'][0]['message']['content']
                Chatbot.previous = answer[3:].lstrip()
            messages = [
                {"role": "system", "content": Chatbot.previous},
                {"role": "user", "content": f"{ctx.author}: {arg}"}
            ]
            Chatbot.previous += f"\n{ctx.author}: {arg}"
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages
        )
        answer = response['choices'][0]['message']['content']
        if answer.startswith("AI:"):
            Chatbot.previous += f"\n{answer.lstrip()}"
            await ctx.respond(answer[3:])
        else:
            Chatbot.previous += f"\nAI: {answer.lstrip()}"
            await ctx.respond(answer)
        print(Chatbot.previous)
        Chatbot.currently_working = False

def setup(bot):
    bot.add_cog(Chatbot(bot))
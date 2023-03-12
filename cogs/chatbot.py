import discord
from discord.ext import commands
import os
import openai
class Chatbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        Chatbot.chat_dict = {}
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.channel.id in Chatbot.chat_dict:
            if ctx.author.bot:
                return
            if len(ctx.content) > 100:
                await ctx.channel.send("100자 이내로 입력해주세요.")
            chat = Chatbot.chat_dict[ctx.channel.id]
            if chat.currently_working is not None:
                return
            answer = chat.chat(str(ctx.author), ctx.content)
            await ctx.channel.send(answer)
            chat.currently_working = None
        else:
            return
    @classmethod
    def can_chat_increase(cls):
        if len(Chatbot.chat_dict) <= 1:
            return True
        else:
            return False
    @discord.slash_command()
    async def 챗봇(self, ctx):
        if ctx.channel.id in Chatbot.chat_dict:
            del Chatbot.chat_dict[ctx.channel.id]
            await ctx.respond("챗봇을 종료합니다.")
            return
        else:
            if Chatbot.can_chat_increase():
                Chatbot.chat_dict[ctx.channel.id] = Chat(ctx.channel.id, os.getenv("OPENAI_API_KEY"))
                await ctx.respond(Chatbot.chat_dict[ctx.channel.id].get_latest_message())
                return
            else:
                await ctx.respond("현재 챗봇을 더 늘릴 수 없습니다.")
                return
class Chat:
    def __init__(self, channel_id, openai_api_key):
        self.channel_id = channel_id
        self.previous_chat = [["Lisa", "안녕하세요! 저는 AI 챗봇 Lisa입니다."]]
        self.openai_api_key = openai_api_key
        self.currently_working = None
    def get_latest_message(self):
        return self.previous_chat[-1][-1]
    @staticmethod
    def parse_chat(chat_list):
        message = ""
        for i in chat_list:
            message += f"{i[0]}: {i[1]}\n"
        return message
    def get_response(self, messages):
        openai.api_key = self.openai_api_key
        response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=messages,
                        max_tokens=1000
                    )
        return response['choices'][0]['message']['content']
    def chat(self, author, content):
        self.currently_working = author
        message_length = 0
        for i in range(len(self.previous_chat)-1, -1, -1):
            message_length += len(self.previous_chat[i][0])
            message_length += len(self.previous_chat[i][1])
            if message_length > 1500 and self.previous_chat[i][0] == "Lisa":
                message_important = self.previous_chat[i:]
                messages = [
                    {"role": "system", "content": f"다음 대화를 Lisa의 입장에서 500자 정도로 구체적으로 요약해줘. \n{Chat.parse_chat(self.previous_chat)}"}
                ]
                self.previous_chat = []
                self.previous_chat.append(["", self.get_response(messages)])
                self.previous_chat.extend(message_important)
                break

        messages = [
            {"role": "system", "content": f"{Chat.parse_chat(self.previous_chat)}"},
            {"role": "user", "content": f"{author}: {content}"}
        ]
        answer = self.get_response(messages)
        if answer.startswith("Lisa:"):
            answer = answer[5:].lstrip()
        self.previous_chat.append([author, content])
        self.previous_chat.append(["Lisa", answer])
        return answer

def setup(bot):
    bot.add_cog(Chatbot(bot))
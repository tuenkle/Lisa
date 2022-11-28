import discord
import yt_dlp
import os
from dotenv import load_dotenv
class LisaDaughter(discord.Client):
    async def on_ready(self):
        print({self.user})

    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.content.startswith('$'):
            striped_message = message.content[1:].lstrip()
            if striped_message.startswith('노래'):
                striped_message = striped_message[2:].lstrip()
                if striped_message in ['', '접속', '들어와']:
                    await message.author.voice.channel.connect()
                    await message.channel.send('보이스 채널에 접속합니다.')
                if striped_message.startswith('재생'):
                    url = striped_message[2:].lstrip()
                    ffmpeg_options = {'options': '-vn'}
                    ydl_opts = {'format': 'bestaudio',
                                'outtmpl': 'song/temp'}
                    try:
                        os.remove('song/temp')
                    except:
                        pass
                    try:
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            song_info = ydl.download(url)
                            print(song_info)
                    except:
                        await message.channel.send('유효한 주소가 아니거나 다운에 오류가 생겼습니다.')
                        return
                    if client.voice_clients:
                        voice_client = client.voice_clients[0]
                    else:
                        try:
                            voice_client = await message.author.voice.channel.connect()
                        except Exception as e:
                            print(e)
                            await message.channel.send('유저가 보이스 채널에 접속 중이지 않습니다.')
                            return
                    try:
                        if voice_client.is_playing or voice_client.is_paused:
                            voice_client.stop()
                        voice_client.play(discord.FFmpegOpusAudio('song/temp', executable='ffmpeg', **ffmpeg_options))
                        await message.channel.send('노래를 재생합니다.')
                    except Exception as e:
                        print(e)
                        await message.channel.send('재생에 문제가 생겼습니다.')
                elif striped_message.startswith('중지') or striped_message.startswith('중단'):
                    if client.voice_clients:
                        voice_client = client.voice_clients[0]
                        if voice_client.is_playing():
                            voice_client.pause()
                            await message.channel.send('노래를 중지합니다.')
                        else:
                            await message.channel.send('노래를 재생 중이지 않습니다.')
                    else:
                        await message.channel.send('보이스 채널에 접속 중이지 않습니다.')
                elif striped_message.startswith('재개'):
                    if client.voice_clients:
                        voice_client = client.voice_clients[0]
                        if voice_client.is_paused():
                            voice_client.resume()
                            await message.channel.send('노래를 재개합니다.')
                        else:
                            await message.channel.send('노래를 중지되어 있지 않습니다.')
                    else:
                        await message.channel.send('보이스 채널에 접속 중이지 않습니다.')
                elif striped_message.startswith('종료') or striped_message.startswith('나가'):
                    if client.voice_clients:
                        voice_client = client.voice_clients[0]
                        if voice_client.is_playing or voice_client.is_paused:
                            voice_client.stop()
                        await voice_client.disconnect()
                        await message.channel.send('보이스 채널에서 나갑니다.')
                    else:
                        await message.channel.send('보이스 채널에 접속 중이지 않습니다.')
            else:
                await message.channel.send('안녕하세요')

intents = discord.Intents.all()
client = LisaDaughter(intents=intents)
load_dotenv()

client.run(os.environ.get("LISA_TOKEN"))
import discord  # Библиотека для работы с API Дискорда
from discord.ext import commands

from youtube_dl import YoutubeDL  # Библиотека для работы с Youtube


class music_bot(commands.Cog):  # Это код самого функционала бота
    def __init__(self, bot):
        self.bot = bot

        # Статус воспроизведения
        self.is_playing = False

        # создание двухмерного списка, состоящего из песни и канала, добавление опций для работы на Youtube
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}

        self.vc = ""

    # находим музыку на Youtube
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            # ссылка на музыку или запрос
            m_url = self.music_queue[0][0]['source']

            # Убираем первый трек, который проигрываем
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    # проверяем на зацикливание
    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            # Пытаемся войти на канал, если мы ещё не там

            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await self.music_queue[0][1].connect()
            else:
                await self.vc.move_to(self.music_queue[0][1])

            print(self.music_queue)
            # убираем первый трек, который проигрываем
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    @commands.command(name="play")
    async def p(self, ctx, *args):
        query = " ".join(args)

        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            # Нужно находиться на канале, чтобы бот знал, куда идти
            await ctx.send("Сперва зайдите на любой голосовой канал!")
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send(
                    "Невозможно загрузить трек, проверьте правильность написания. Возможно, Вы пытаетесь запустить стрим или плейлист.")
            else:
                await ctx.send("Трек добавлен в очередь")
                self.music_queue.append([song, voice_channel])

                if self.is_playing == False:
                    await self.play_music()

    @commands.command(name="queue")
    async def q(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += self.music_queue[i][0]['title'] + "\n"

        print(retval)
        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("Очередь пуста")

    @commands.command(name="skip")
    async def skip(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()
            # Пробуем запустить следующий трек, если он, конечно, есть
            await self.play_music()
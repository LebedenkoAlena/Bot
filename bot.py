import discord
from discord.ext import commands

import os

from music_bot import music_bot

bot = commands.Bot(command_prefix='/')

# Регистрируем класс у бота
bot.add_cog(music_bot(bot))

# Запускаем с моего токена
bot.run('ODM0ODE5MTcwMTg4Nzg3NzEz.YIGb8A.mauKlPkkLqr9zXJGrL30QLtyzHw')

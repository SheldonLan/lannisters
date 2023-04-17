from nextcord.ext import commands

import secret

bot = commands.Bot()

bot.run(secret.key)
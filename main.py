from bot import Cryptrans
from os import environ


bot = Cryptrans()

extensions = []

for extension in extensions:
    bot.load_extension(extension)


bot.run(environ['BOT_TOKEN'])

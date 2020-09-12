from bot import Cryptrans
from os import environ


bot = Cryptrans()

controllers = [
    "crypto_create_controller",
    "crypto_info_controller",
]

for controller in controllers:
    bot.load_extension("controllers." + controller)


bot.run(environ['BOT_TOKEN'])

from bot import VirtualCrypto
from os import environ


bot = VirtualCrypto()

controllers = [
    "crypto_create_controller",
    "crypto_info_controller",
    "crypto_give_controller",
    "user_info_controller",
    "help_command_controller",
]

for controller in controllers:
    bot.load_extension("controllers." + controller)


bot.run(environ['BOT_TOKEN'])

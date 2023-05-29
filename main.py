from private import authorization, config
import parser
import sql as bd
from BOT import bot

def start_parser():
    susu = parser.pars()
    susu.get_authorization(authorization.login, authorization.password)
    susu.enter_to_schedule()
    susu.enter_to_start_of_semester()

def bot_run():
    bot.bot.run()

if __name__ == '__main__':
    bot_run()




from aiogram import Bot,Dispatcher,types
from config import TOKEN
from commands import register_user_commands

bot=Bot(token=TOKEN)
dp=Dispatcher()


register_user_commands(dp)

if __name__ =='__main__':
	dp.run_polling(bot)
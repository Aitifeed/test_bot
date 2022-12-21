__all__=['register_user_commands']

from aiogram import Router,F
from commands.start import start#,get_file_id
from aiogram.filters.command import Command
from handlers.callback import start_replenishment,choice_action,change_balance,ban_unban_user
from commands.qiwi_actions import create_qiwi_account,link_payment,status_pay
from States import Sum,change_data_user
from admin_commands.admin_action import check_user_and_balance,final_change_balance
from callback_factories import data_user_CD,data_for_new_balance,data_for_ban

def register_user_commands(router:Router):
	router.message.register(start,Command(commands=['start']))
	router.message.register(create_qiwi_account,Sum.amount_from_user)
	router.message.register(link_payment,F.text=='Ссылка на оплату счёта')
	router.message.register(status_pay,F.text=='Проверка состояния платежа')
	router.message.register(check_user_and_balance,F.text=='Посмотреть всех пользователей с их балансом')
	router.message.register(final_change_balance,change_data_user.balance)

	router.callback_query.register(start_replenishment,F.data=='top_up_balance')
	router.callback_query.register(choice_action,data_user_CD.filter())
	router.callback_query.register(change_balance,data_for_new_balance.filter())
	router.callback_query.register(ban_unban_user,data_for_ban.filter())
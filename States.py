from aiogram.fsm.state import State, StatesGroup

class Sum(StatesGroup):
	amount_from_user=State()
	bill_id=State()
	url_pay=State()

class change_data_user(StatesGroup):
	user_id=State()
	balance=State()
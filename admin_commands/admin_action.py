from aiogram import types,F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup,Message
from aiogram.utils.keyboard import KeyboardBuilder,KeyboardButton,ReplyKeyboardMarkup
from messages import MESSAGES
from States import Sum
from qiwi.authorization_qiwi import p2p
from callback_factories import data_user_CD
from PostgreSQL import Database
from config import working_db,admin_id

async def check_user_and_balance(message:Message):
	if message.from_user.id == admin_id:
		db=Database(working_db)
	
		user_data=db.get_user_data()

		keyboard = KeyboardBuilder(button_type=InlineKeyboardButton)

		for i in user_data:
			keyboard.row(
				InlineKeyboardButton(text='Пользователь - '+i[1]+',баланс - '+str(i[2]),
    						callback_data=data_user_CD(user_id=i[0],balance=i[2],username=i[1],
    											ban=i[3]).pack())
    			)

		await message.answer(text='Выберите пользователя,которому хотите поменять баланс или забанить',
							reply_markup=keyboard.as_markup())
	else:
		return
async def final_change_balance(message:Message,state:FSMContext):
	data=await state.get_data()
	
	db=Database(working_db)
	db.add_new_balance(data['user_id'],int(message.text))

	await message.answer(text='баланс для пользователя @'+data['username']+' успешно изменен на '+message.text)

	await state.clear()
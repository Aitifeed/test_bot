from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import KeyboardBuilder
from aiogram.types import InlineKeyboardButton,Message
from messages import MESSAGES
from callback_factories import data_user_CD,data_for_new_balance,data_for_ban
from States import Sum,change_data_user
from aiogram.types import InlineKeyboardButton
from PostgreSQL import Database
from config import working_db

async def start_replenishment(call:types.callback_query.CallbackQuery,state:FSMContext):
    db=Database(working_db)
    if db.get_ban_user(call.from_user.id)==True:
        await call.message.answer(text='Вы забанены и не можите пользоваться ботом.')
    else:
        await call.message.answer(MESSAGES['msg_relenishment'])
        await state.set_state(Sum.amount_from_user)

async def choice_action(call:types.callback_query.CallbackQuery,callback_data:data_user_CD):
    
    keyboard=KeyboardBuilder(button_type=InlineKeyboardButton)
    keyboard.row(
        InlineKeyboardButton(text='Изменить баланс',
                            callback_data=data_for_new_balance(user_id=callback_data.user_id,
                                                            username=callback_data.username).pack())
        )
    if callback_data.ban==False:
        keyboard.row(
            InlineKeyboardButton(text='Забанить пользовтеля',
                            callback_data=data_for_ban(user_id=callback_data.user_id,
                                                        username=callback_data.username,
                                                        ban=False).pack())
        )
    else:
        keyboard.row(
            InlineKeyboardButton(text='Разбанить пользовтеля',
                            callback_data=data_for_ban(user_id=callback_data.user_id,
                                                        username=callback_data.username,
                                                        ban=True).pack())
        )
    await call.message.answer(text='Выберите дейсвтие для пользователя @'+callback_data.username,
                            reply_markup=keyboard.as_markup())

async def change_balance(call:types.callback_query.CallbackQuery,callback_data:data_for_new_balance,state:FSMContext):
    await call.message.answer(text='Отправьте новую сумму баланса для пользователя @'+callback_data.username)
    
    await state.update_data(user_id=callback_data.user_id,
                            username=callback_data.username)
    await state.set_state(change_data_user.balance)

async def ban_unban_user(call:types.callback_query.CallbackQuery,callback_data:data_for_ban):
    db=Database(working_db)
    
    if callback_data.ban==False:
        db.ban_unban_user_db(callback_data.user_id, True)
        await call.message.answer(text='Поьзователь @'+callback_data.username+' забанен!')
    else:
        db.ban_unban_user_db(callback_data.user_id,False)
        await call.message.answer(text='Поьзователь @'+callback_data.username+' разбанен!')

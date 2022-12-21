from messages import MESSAGES
from aiogram.utils.keyboard import (KeyboardButton,ReplyKeyboardBuilder,KeyboardBuilder)
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup,Message,ReplyKeyboardRemove,ReplyKeyboardMarkup
from config import admin_id,user,working_db
from PostgreSQL import Database

async def start(message:Message):
    if message.from_user.id == admin_id:
        db=Database(working_db)
        db.create_database_and_table()

        keyboard = KeyboardBuilder(button_type=KeyboardButton)
        keyboard.add(
            KeyboardButton(text='Посмотреть всех пользователей с их балансом'),
            KeyboardButton(text='Посмотреть логи')
        )

        s_builder=ReplyKeyboardMarkup(keyboard=keyboard.export(),resize_keyboard=True)
        
        await message.answer(text='Админка',reply_markup=s_builder)
    
    else:
        db=Database(working_db)

        if db.get_ban_user(message.from_user.id)==True:
            await message.answer(text='Вы забанены и не можите пользоваться ботом.')
        else:
            await message.answer(MESSAGES['msg_start'].format(message.from_user.first_name),
                            reply_markup=ReplyKeyboardRemove())
        
            if message.chat.type=='private':
                if not db.user_exists(message.from_user.id):
                    if message.from_user.username==None:
                        db.add_user(message.from_user.id,message.from_user.first_name)
                    else:    
                        db.add_user(message.from_user.id,message.from_user.username)


            keyboard = KeyboardBuilder(button_type=InlineKeyboardButton)
            keyboard.row(
                InlineKeyboardButton(text='Пополнить баланс',callback_data='top_up_balance')
                )
        
            await message.answer(MESSAGES['msg_to_user'],reply_markup=keyboard.as_markup())
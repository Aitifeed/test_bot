from aiogram import types,F
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import KeyboardBuilder,KeyboardButton,ReplyKeyboardMarkup
from aiogram.types import Message,ReplyKeyboardRemove
from messages import MESSAGES
from States import Sum
from qiwi.authorization_qiwi import p2p
import random
import asyncio
from PostgreSQL import Database
from config import working_db

async def create_qiwi_account(message:Message,state:FSMContext):
    try:
        int(message.text)
        keyboard = KeyboardBuilder(button_type=KeyboardButton)
        keyboard.add(
            KeyboardButton(text='Ссылка на оплату счёта'),
            KeyboardButton(text='Проверка состояния платежа')
        )
        
        new_bill=p2p.bill(amount=message.text,
                            lifetime=5)
        await state.clear()
        await state.update_data(amount_from_user=int(message.text),
                                bill_id=new_bill.bill_id,
                                pay_url=new_bill.pay_url)

        s_builder=ReplyKeyboardMarkup(keyboard=keyboard.export(),resize_keyboard=True)
    
        await message.answer(MESSAGES['msg_info_payment'].format(new_bill.bill_id),parse_mode='html',
                            reply_markup=s_builder)

        await check_payment(message=message,state=state)

    except ValueError:
        await message.answer('Нужно отправлять только цифры,без текста,пробелов или других символов.\n\nОтправьте повторно нужную вам сумму сюда же')
        await state.set_state(Sum.amount_from_user)
        

async def link_payment(message:Message,state:FSMContext):
    db=Database(working_db)
    if db.get_ban_user(message.from_user.id)==True:
            await message.answer(text='Вы забанены и не можите пользоваться ботом.')
    else:
        data = await state.get_data()
        if len(data)==0:
            await message.answer(text='У вас нет ссылки на счёт,начните пополнять баланс и ссылка по вашему счёту создаться')
        else:
            await message.answer(text='Ваша ссылка на оплату счёта - '+data['pay_url'])

async def status_pay(message:Message,state:FSMContext):
    db=Database(working_db)
    if db.get_ban_user(message.from_user.id)==True:
            await message.answer(text='Вы забанены и не можите пользоваться ботом.')
    else:
        data = await state.get_data()

        if p2p.check(bill_id=data['bill_id']).status=='WAITING':
            await message.answer('Ожидается оплата счёта')
        elif p2p.check(bill_id=data['bill_id']).status=='EXPIRED':
            await message.answer('Время оплаты счёта истекло')
        else:
            await message.answer('Счёт успешно оплачен')

async def check_payment(message:Message,state:FSMContext):
    data = await state.get_data()
    
    db=Database(working_db)
    time_pay=0
    while time_pay<=300:
        if p2p.check(bill_id=data['bill_id']).status=='PAID':
            db.add_balance(message.from_user.id,data['amount_from_user'])
            break


        await asyncio.sleep(10)
        time_pay+=10


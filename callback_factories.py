from aiogram.filters.callback_data import CallbackData

class data_user_CD(CallbackData,prefix='us_bl'):
   user_id:int
   username:str
   balance:int
   ban:bool

class data_for_new_balance(CallbackData,prefix='new_b'):
   user_id:int
   username:str

class data_for_ban(CallbackData,prefix='ban'):
   user_id:int
   username:str
   ban:bool
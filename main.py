import telebot
from telebot import types
import user_db
import loader
import waletlib
import function


bot = telebot.TeleBot('6025512148:AAHaIGG7KydSTw_TfrdhS3limxUQ3mqxiyE')


@bot.message_handler(commands=["start"])
def start(message):
    print(message.text)
    if message.text == "/start":
        pass
    elif message.text == "0":
        print(1)







@bot.message_handler(commands=["mywallets"])
def my_wallet(message):
    wallets = user_db.check_wallets(message.chat.id)
    if wallets:
        keyboard = types.InlineKeyboardMarkup()
        for wallet in wallets:

            keyboard.add(types.InlineKeyboardButton(text=wallet[0], callback_data=f"wallet/check/{wallet[1]}"))




        bot.send_message(message.chat.id, "выберите кошелек", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "у вас еще нет кошельков\nдля создания кошелька введите /newwallet")

#
#
#
#
#
#
#
@bot.message_handler(commands=["newwallet"])
def new_wallet(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="рандомное название", callback_data=f"new_wallet/yes/rand/{message.chat.id}"))
    keyboard.add(types.InlineKeyboardButton(text="ваше название", callback_data=f"new_wallet/yes/unrand/{message.chat.id}"))
    keyboard.add(types.InlineKeyboardButton(text="назад", callback_data=f"new_wallet/"))
    bot.send_message(message.chat.id, "выбирите?", reply_markup=keyboard)


#
#
#
#
#
#
#
#
# @bot.message_handler(commands=["createcheque"])




@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    print(call.data)
    if call.data.split("/")[0] == "new_wallet":
        bot.clear_step_handler_by_chat_id(call.message.chat.id)
        if call.data.split("/")[1] == "yes":
            if call.data.split("/")[2] == "rand":
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                wal = waletlib.create_wallet()
                user_db.add_wallet(function.create_wallet(), call.data.split("/")[3], wal["pub"], wal["priv"])
                bot.send_message(call.message.chat.id, "кошелек создан")
            elif len(user_db.check_wallets(call.data.split("/")[2])) != loader.max_free_wallets and call.data.split("/")[2] == "unrand":
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton(text="рандомное название", callback_data=f"new_wallet/yes/rand/{call.data.split('/')[3]}"))
                keyboard.add(types.InlineKeyboardButton(text="назад", callback_data=f'new_wallet/back'))
                m = bot.send_message(call.message.chat.id, "введите название", reply_markup=keyboard)
                bot.register_next_step_handler(m, reg_wallet, call.data.split("/")[3])

        elif call.data.split("/")[1] == "no":
            bot.clear_step_handler_by_chat_id(call.message.chat.id)
        elif call.data.split("/")[1] == "back":
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            new_wallet(call.message)
    elif call.data.split("/")[0] == "wallet":
        if call.data.split("/")[1] == "check":
            bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)
            wallet = user_db.get_wallet(call.message.chat.id, call.data.split("/")[2])
            w = waletlib.wallet(call.data.split("/")[2], wallet[2])
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text='удалить кошелек', callback_data=f'wallet/delete/none/{call.data.split("/")[2]}'))
            keyboard.add(types.InlineKeyboardButton(text='переслать деньги', callback_data=f'wallet/send/none/{call.data.split("/")[2]}'))

            bot.send_message(call.message.chat.id, f"{wallet[3]}\n{w.check_amount()}", reply_markup=keyboard)
        elif call.data.split("/")[1] == 'delete':
            if call.data.split("/")[2] == "none":
                bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton("да", callback_data=f'wallet/delete/yes/{call.data.split("/")[3]}'))
                keyboard.add(types.InlineKeyboardButton("назад", callback_data=f'wallet/check'))
                bot.send_message(call.message.chat.id, "вы уверены", reply_markup=keyboard)
            elif call.data.split("/")[2] == 'yes':
                bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)
                user_db.delete_wallet(user_id=call.message.chat.id, pub_key=call.data.split("/")[3])
                bot.send_message(call.message.chat.id, 'кошелек удален')
        elif call.data.split("/")[1] == 'send':
            if call.data.split("/")[2] == "none":
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton("создать чек", callback_data=f'wallet/cheque/{call.data.split("/")[3]}'))
                keyboard.add(types.InlineKeyboardButton("переслать деньги чек", callback_data=f'wallet/send/yes/{call.data.split("/")[3]}'))
            elif call.data.split("/")[2] == 'yes':
                m = bot.send_message(call.message.chat.id, "пришлите pub key кошелька")
                bot.register_next_step_handler(m, send_money)


def send_money(message, user_pub_key):
    pass




def reg_wallet(message, id):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="назад", callback_data=f"new_wallet/no"))
    wal = waletlib.create_wallet()
    user_db.add_wallet(message.text, id, wal["pub"], wal["priv"])
    bot.send_message(message.chat.id, "кошелек создан", reply_markup=keyboard)


bot.polling(none_stop=True)


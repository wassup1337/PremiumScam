import telebot
from telebot import types
import random
from settings import *
from database import *

bot = telebot.TeleBot(TOKEN)

markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
work = types.KeyboardButton(text="⭐️ Заработать шансы")
roll = types.KeyboardButton(text="🎰 Крутить рулетку")
profile = types.KeyboardButton(text='🤑 Мой профиль')
exs = types.KeyboardButton(text="💰 Задания")
markup2.row(work, roll)
markup2.row(profile)
markup2.row(exs)

@bot.message_handler(commands=['start'])
def handle_start(message):
    args = message.text.split()
    user_id = message.from_user.id
    username = message.from_user.username or f"User{user_id}"
    ref_link = f"https://t.me/{bot.get_me().username}?start={user_id}"
    markup = types.InlineKeyboardMarkup()
    share = types.InlineKeyboardButton(text="Поделиться ссылкой", switch_inline_query=ref_link)
    markup.add(share)
    
    start = types.BotCommand(command='start', description='♻️ Перезапустить бота')
    why = types.BotCommand(command='why', description='🚀 Зачем нужен Telegram Premium?')

    bot.set_my_commands([start, why])
    bot.set_chat_menu_button(
    chat_id=message.chat.id,
    menu_button=types.MenuButtonCommands()
    )
    
    if not user_exists(user_id):
        referral_id = None
        if len(channel_ids) > 0:
            if check_subscription(user_id, channel_ids):
                return
            
        if len(args) > 1 and args[1].isdigit():
            referral_id = int(args[1])
            if user_exists(referral_id):
                bot.send_message(referral_id, f"<b>☑️ По вашей реферальной ссылке перешел новый пользователь.\n\nВаш шанс повышен на 0.1 %\n\nПерешли ссылку — {ref_link}</b>", parse_mode='HTML')
                increment_referrals(referral_id)
                increment_chance(referral_id, 0.1)

        add_user(user_id, username, referral_id)
        bot.send_message(user_id, "⭐", reply_markup=markup2)
        bot.send_message(user_id, f"<b>✨ Добро пожаловать!\n\nРаспространяй свою ссылку и получи Telegram Premium за приглашенных друзей\n\n🔗 Ваша ссылка - {ref_link}</b>", parse_mode='HTML', reply_markup=markup)
    else:
        if len(channel_ids) > 0:
            if check_subscription(user_id, channel_ids):
                return
        bot.send_message(user_id, "⭐", reply_markup=markup2)
        bot.send_message(user_id, f"<b>✨ Добро пожаловать!\n\nРаспространяй свою ссылку и получи Telegram Premium за приглашенных друзей\n\n🔗 Ваша ссылка - {ref_link}</b>", parse_mode='HTML', reply_markup=markup)
@bot.message_handler(commands=['why'])
def handle_why(message):
    user_id = message.from_user.id
    ref_link = f"https://t.me/{bot.get_me().username}?start={user_id}"
    if user_exists(user_id):
        bot.send_message(user_id, f"💎 <b>Почему стоит выбрать Telegram Premium?</b>\n\n"
                                  f"🔓 <b>Доступ к эксклюзивным функциям:</b>\n"
                                  f"• Улучшенная скорость загрузки сообщений\n"
                                  f"• Уникальные стикеры и темы оформления\n"
                                  f"• Приоритетная поддержка и еще многое другое!\n\n"
                                  f"🚀 <b>Быстрее и удобнее:</b>\n"
                                  f"• Без рекламы\n"
                                  f"• Больше возможностей для работы с файлами\n"
                                  f"• Режим офлайн для сохранения сообщений\n\n"
                                  f"🌟 <b>Выделись среди остальных пользователей:</b>\n"
                                  f"• Эксклюзивные эмодзи\n"
                                  f"• Возможность использования анимированных аватарок\n"
                                  f"• Режим «Не беспокоить» на разных устройствах одновременно\n\n"
                                  f"🎉 <b>Премиум — это не просто подписка, а новый уровень использования Telegram!</b>\n\n"
                                  f"<i>Пересылай свою ссылку — {ref_link}</i>", parse_mode='HTML')
    else:
        bot.send_message(user_id, "Сначала используйте команду /start, чтобы зарегистрироваться.")
        

@bot.message_handler(commands=['adminpanel'])
def adminpanel(message):
    if message.from_user.id in admins:
        admin_markup = types.InlineKeyboardMarkup(row_width=2)
        add_chance = types.InlineKeyboardButton(text="⭐️ Выдать шансы", callback_data="add_chance")
        remove_chance = types.InlineKeyboardButton(text="⭐️ Снять шансы", callback_data="remove_chance")
        mailing = types.InlineKeyboardButton(text="📨 Рассылка", callback_data="mailing")
        add_channel = types.InlineKeyboardButton(text="📚 Добавить канал", callback_data="add_channel")
        remove_channel = types.InlineKeyboardButton(text="🚫 Удалить канал", callback_data='delete_channel')
        mailing_zero_refs = types.InlineKeyboardButton(text="📨 Рассылка 0 реф", callback_data='mailing_zero_refs')
        
        admin_markup.row(add_chance, remove_chance)
        admin_markup.row(mailing)
        admin_markup.row(add_channel, remove_channel)
        admin_markup.row(mailing_zero_refs)
        bot.send_message(message.chat.id, f"<b>📊 Админ-панель\n\n👥 Пользователей: {get_user_count()}</b>", parse_mode='HTML', reply_markup=admin_markup)

@bot.message_handler(func=lambda message: True)
def hadnler_reply_buttons(message):
    user_id = message.from_user.id
    ref_link = f"https://t.me/{bot.get_me().username}?start={user_id}"
    
    if message.text == "⭐️ Заработать шансы":
        markup = types.InlineKeyboardMarkup()
        share = types.InlineKeyboardButton(text="Поделиться ссылкой", switch_inline_query=ref_link)
        markup.add(share)
        bot.send_message(message.chat.id, f"<b>🎉 Приглашай друзей, знакомых и получай +0.1 % шанса за каждого!\n\nКидай ссылку:\n\n• в ЛС знакомым\n• в свой телеграм канал\n• по чужим группам\n• в комментариях тик тока\n• вк/инст/ватсап и др. соц сети\n\n🔗 Ваша ссылка - {ref_link}</b>", parse_mode='HTML', reply_markup=markup)
    elif message.text == "🎰 Крутить рулетку":
        user_data = get_user(user_id)
        if user_data:
            chance = get_user_chance(user_id)
            randozed = random.randint(70, 100)
            if randozed <= chance:
                bot.send_message(message.chat.id, "<b>🎉 Поздравляю!\n\nВы выиграли Telegram Premium!\n\nОжидайте оповщения от администратора.</b>", parse_mode='HTML')
                detele_chances(user_id, 0)
                for admin in admins:
                    bot.send_message(admin, f"<b>✅ Пользователь @{user_data[1]} | {user_data[0]} выиграл Telegram Premium!</b>", parse_mode='HTML')
            else:
                detele_chances(user_id, 0)
                bot.send_message(message.chat.id, f"<b>❌ К сожалению, вы не выиграли Telegram Premium.\n\nВыпало: {randozed}%\n\nВаши шансы: {chance}%</b>", parse_mode='HTML')
    elif message.text == "🤑 Мой профиль":
        user_data = get_user(user_id)
        if user_data:
            count_refs = user_data[3]
            chance = str(user_data[2])
            rolled = user_data[5]
            bot.send_message(user_id, f"<b>🎉 Шансы: {chance[:4]}%\n\nПриглашенных пользователей: {count_refs}\n\n🎲 Прокручено: {rolled} раз\n\n🔗 Ваша ссылка - {ref_link}</b>", parse_mode='HTML')
        else:
            bot.send_message(user_id, "<b>❌ Ваш профиль не найден. Используйте /start для регистрации.</b>", parse_mode='HTML')
    elif message.text == "💰 Задания":
        bot.send_message(user_id, "<b>🎯 На данный момент нет доступных заданий!\n\nВозвращайся позже!</b>", parse_mode='HTML')
    else:
        bot.send_message(user_id, f"<b>❌ Неизвестная команда!</b>", parse_mode='HTML', reply_markup=markup2)
        
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    user_id = call.from_user.id
    ref_link = f"https://t.me/{bot.get_me().username}?start={user_id}"
    username = call.from_user.username
    
    if call.data == "add_chance":
         bot.send_message(user_id, "<b>Введите ID пользователя и шанс для добавления в формате:\nID:Количество</b>", parse_mode='HTML')
         bot.register_next_step_handler(call.message, add_chance)
    if call.data == "remove_chance":
         bot.send_message(user_id, "<b>Введите ID пользователя и шанс для удаления в формате:\nID:Количество</b>", parse_mode='HTML')
         bot.register_next_step_handler(call.message, delete_chance)
    if call.data == "mailing":
         bot.send_message(user_id, "<b>Введите текст для рассылки:</b>", parse_mode='HTML')
         bot.register_next_step_handler(call.message, send_mailing)
    if call.data == "add_channel":
        bot.send_message(user_id, "<b>Введите ID канала:</b>", parse_mode='HTML')
        bot.register_next_step_handler(call.message, add_channel)
    if call.data == 'delete_channel':
        bot.send_message(user_id, "<b>Введите ID канала:</b>", parse_mode='HTML')
        bot.register_next_step_handler(call.message, delete_channel)
    if call.data == 'mailing_zero_refs':
        text = "⁉️🤨Мы заметили, что вы не пригласили ни 1 друга!\n\nПерешли ссылку своим друзьям, а также по чатам, добавляется 0.1% шансов за 1 приглашенного⤵️"
        users = get_user_zero_referrals()
         
        for user in users:
             user_id = user[0]
             ref_link = f"\n\nТвоя персональная ссылка — https://t.me/{bot.get_me().username}?start={user_id}"
             full_text = f"{text}{ref_link}"
             
             try:
                 bot.send_message(user_id, f"<b>{full_text}</b>", parse_mode='HTML')
                 print(f"[РАССЫЛКА 1.0] Отправлено: {user_id}")
             except Exception as e:
                 print(f"[РАССЫЛКА 1.0] Не отправлено: {user_id}")
    if call.data == "check_subs":
        user_id = call.from_user.id
        markup = types.InlineKeyboardMarkup()
        share = types.InlineKeyboardButton(text="Поделиться ссылкой", switch_inline_query=ref_link)
        markup.add(share)
        if check_subscription(user_id, channel_ids):
            return
        bot.send_message(user_id, "⭐", reply_markup=markup2)
        bot.send_message(user_id, "<b>✨ Добро пожаловать!\n\nРаспространяй свою ссылку и получи Telegram Premium за 1 приглашенного друга</b>", parse_mode='HTML', reply_markup=markup)
        
def delete_channel(message):
    try:
        channel_id = int(message.text)
        if channel_id in channel_ids:
            channel_ids.remove(channel_id)
            bot.send_message(message.chat.id, "<b>✅ Канал успешно удален!</b>", parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, "<b>❌ Канал не найден!</b>", parse_mode='HTML')
    except ValueError:
        bot.send_message(message.chat.id, "<b>❌ Некорректный ID канала!</b>", parse_mode='HTML')

def add_channel(message):
    try:
        channel_id = int(message.text)
        channel_ids.append(channel_id)
        bot.send_message(message.chat.id, "<b>✅ Канал успешно добавлен!</b>", parse_mode='HTML')
    except ValueError:
        bot.send_message(message.chat.id, "<b>❌ Некорректный ID канала!</b>", parse_mode='HTML')

def add_chance(message):
    try:
        user_id, chance = map(int, message.text.split(':'))
        increment_chance(user_id, chance)
        bot.send_message(message.chat.id, f"<b>✅ {chance} шансов успешно добавлено пользователю с ID {user_id}</b>", parse_mode='HTML')
        bot.send_message(user_id, f"✅ Администратор добавил вам {chance} шансов!", parse_mode='HTML')
    except ValueError:
        bot.send_message(message.chat.id, "<b>❌ Неверный формат. Пожалуйста, введите ID и количество шансов в формате ID:Количество</b>", parse_mode='HTML')

def delete_chance(message):
    try:
        user_id, chance = map(int, message.text.split(':'))
        detele_chances(user_id, chance)
        bot.send_message(message.chat.id, f"<b>✅ {chance} шансов успешно удалено у пользователя с ID {user_id}</b>", parse_mode='HTML')
        bot.send_message(user_id, f"✅ Администратор удалил у вас {chance} шансов!", parse_mode='HTML')
    except ValueError:
        bot.send_message(message.chat.id, "<b>❌ Неверный формат. Пожалуйста, введите ID и количество шансов в формате ID:Количество</b>", parse_mode='HTML')

def send_mailing(message):
    text = message.text
    users = get_users()
    counter = 0

    for user in users:
        user_id = user[0]
        ref_link = f"\n\nТвоя персональная ссылка — https://t.me/{bot.get_me().username}?start={user_id}"
        full_text = f"{text}{ref_link}"
        
        try:
            counter += 1
            bot.send_message(user_id, f"<b>{full_text}</b>", parse_mode='HTML')
            print(f"[РАССЫЛКА] Отправлено: {user_id}")
        except Exception as e:
            print(f"[РАССЫЛКА] Не отправлено: {user_id}")

def check_subscription(user_id, channel_ids):
    
    if not channel_ids:
        return True

    markup = types.InlineKeyboardMarkup()
    for channel_id in channel_ids:
        try:
            chat_member = bot.get_chat_member(channel_id, user_id)
            if chat_member.status not in ['member', 'administrator', 'creator']:
                invite_link = bot.create_chat_invite_link(channel_id, member_limit=1).invite_link
                subscribe_button = types.InlineKeyboardButton("Подписаться", url=invite_link)
                markup.add(subscribe_button)
        except Exception as e:
            print(f"Ошибка при проверке подписки: {e}")
            bot.send_message(user_id, "Ошибка при проверке подписки. Пожалуйста, попробуйте позже.")
            return False

    if markup.keyboard:
        check_button = types.InlineKeyboardButton("✅ Проверить подписку", callback_data="check_subs")
        markup.add(check_button)
        bot.send_message(user_id, "<b>👋🏻 Добро пожаловать\n\nПодпишитесь на каналы, чтобы продолжить!</b>", parse_mode='HTML', reply_markup=markup)
        return True

    return False

if __name__ == '__main__':
    bot.infinity_polling()
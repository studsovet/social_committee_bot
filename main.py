import telebot
import vk_api
import random
from gsheets import GSheets
from user import User
from keyboard import Keyboard
from bot_messages import BotMessages
from manager_photo import ManagerPhoto

token = "e28bf8d579d53aafd83a26361b662b11d1475c810443de2baea4e0fc20a2ae3de0319d1b8f7ed19905e88"
vk = vk_api.VkApi(token=token)
chat_id = 1  # id беседы

bot = telebot.TeleBot("2002661300:AAFiaJMl0qs9n_9Foy1jLhe1QQXKmaXXcow")
keyboard = Keyboard()
bot_messages = BotMessages()
manager_photo = ManagerPhoto()

gsheets = GSheets()


def write_msg_vk_bot(message):
    vk.method('messages.send', {'chat_id': chat_id, 'message': message, 'random_id': random.randint(0, 2048)})


@bot.message_handler(commands=['start'])
def start_message(message):
    bot_messages.set_language('Русский')  # Язык по умлочанию
    keyboard.set_language('Русский')  # Язык по умлочанию
    user = User(message.chat.id, message.chat.first_name, message.chat.username)
    bot.send_message(message.chat.id, bot_messages.start_message(), reply_markup=keyboard.kb_language())
    bot.register_next_step_handler(message, choose_language, user)


def choose_language(message, user):
    if message.text in keyboard.language + keyboard.back[keyboard.lang]:
        user.add_language(message.text)  # Устанавливаем язык для всех сообщений
        bot_messages.set_language(user.language)
        keyboard.set_language(user.language)
        manager_photo.set_language(user.language)
        bot.send_photo(message.chat.id, manager_photo.get_welcome_photo())
        bot.send_message(message.chat.id, bot_messages.problems(),
                         reply_markup=keyboard.kb_problem_area())
        bot.register_next_step_handler(message, choose_problem_area, user)
    else:
        bot.send_message(message.chat.id, bot_messages.error())
        bot.register_next_step_handler(message, choose_language, user)


def choose_problem_area(message, user):
    if message.text in keyboard.problem_area[keyboard.lang]:
        user.add_problem_area(message.text)
        if user.problem_area in ['Соц. обеспечение', 'Учебный корпус', 'Dormitory', 'Campus']:
            bot.send_message(message.chat.id, bot_messages.choose_problem(),
                             reply_markup=keyboard.kb_infrastructure())
            bot.register_next_step_handler(message, choose_problem, user)
        elif user.problem_area in ['Столовая', 'Cafeteria']:
            bot.send_message(message.chat.id, bot_messages.choose_problem(),
                             reply_markup=keyboard.kb_food())
            bot.register_next_step_handler(message, choose_problem, user)
        elif user.problem_area in ['Другое', 'Other']:
            user.add_problem(message.text)
            bot.send_message(message.chat.id, bot_messages.choose_campus(), reply_markup=keyboard.kb_campuses())
            bot.register_next_step_handler(message, choose_campus, user)
    elif message.text in keyboard.back[keyboard.lang]:
        start_message(message)
    else:
        bot.send_message(message.chat.id, bot_messages.error())
        bot.register_next_step_handler(message, choose_problem_area, user)


def choose_problem(message, user):
    if message.text in keyboard.food[keyboard.lang] + keyboard.infrastructure[keyboard.lang]:
        user.add_problem(message.text)
        print(user.problem)
        bot.send_message(message.chat.id, bot_messages.choose_campus(), reply_markup=keyboard.kb_campuses())
        bot.register_next_step_handler(message, choose_campus, user)
    elif message.text in keyboard.back[keyboard.lang]:
        print("Я нажалась!")
        choose_language(message, user)
    else:
        bot.send_message(message.chat.id, bot_messages.error())
        bot.register_next_step_handler(message, choose_problem, user)


def choose_campus(message, user):
    if message.text in keyboard.campuses[keyboard.lang]:
        user.add_campus(message.text)
        bot.send_photo(message.chat.id, manager_photo.get_tell_problem_photo())
        bot.send_message(message.chat.id, bot_messages.tell_problems(), reply_markup=keyboard.kb_next())
        bot.register_next_step_handler(message, bloc_text_problem, user)
    elif message.text in keyboard.back[keyboard.lang]:
        print("Нажался")
        message.text = user.problem_area
        bot.send_message(message.chat.id, bot_messages.problems(),
                         reply_markup=keyboard.kb_problem_area())
        bot.register_next_step_handler(message, choose_problem_area, user)
    else:
        bot.send_message(message.chat.id, bot_messages.error())
        bot.register_next_step_handler(message, choose_campus, user)


def bloc_text_problem(message, user):
    if message.text not in keyboard.next[keyboard.lang] + keyboard.back[keyboard.lang]:
        if type(message.text) is str:
            user.add_text_problem(message.text + '\n')
            print(message.text)
        else:
            print(type(message.text))
            bot.send_message(message.chat.id, bot_messages.pls_send_text())
        bot.register_next_step_handler(message, bloc_text_problem, user)
    elif message.text in keyboard.back[keyboard.lang]:
        message.text = user.problem
        print(message.text)
        choose_problem(message, user)
    else:
        bot.send_photo(message.chat.id, manager_photo.get_contact_photo())
        bot.send_message(message.chat.id, bot_messages.user_contact(),
                         reply_markup=keyboard.kb_next())
        bot.register_next_step_handler(message, user_contact, user)


def user_contact(message, user):
    if message.text not in keyboard.next[keyboard.lang] + keyboard.back[keyboard.lang]:
        if type(message.text) is str:
            user.add_contact(message.text + ' \n')
        else:
            bot.send_message(message.chat.id, bot_messages.pls_send_text())
        bot.register_next_step_handler(message, user_contact, user)
    elif message.text in keyboard.back[keyboard.lang]:
        print(user.text_problem)
        message.text = user.campus
        choose_campus(message, user)
    else:
        bot.send_photo(message.chat.id, manager_photo.get_bye_photo())
        bot.send_message(message.chat.id, bot_messages.bye())
        gsheets.write_user_to_gsheet(user.chat_id, user.name, user.username, user.campus, user.problem_area,
                                     user.problem, user.contact, user.text_problem, user.language)
        write_msg_vk_bot('Пришла новая заявка №{}. Тема проблемы: {}'.format(gsheets.get_count_applications(),
                                                gsheets.get_cell('E{}'.format(gsheets.get_count_applications() + 1))))
        bot.register_next_step_handler(message, start_message)


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.infinity_polling()

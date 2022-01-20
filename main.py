import vk_api
import random
import asyncio
import logging
import db
from gsheets import GSheets
from user import User
from keyboard import Keyboard
from bot_messages import BotMessages
from manager_photo import ManagerPhoto
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

token_tg = "2002661300:AAFiaJMl0qs9n_9Foy1jLhe1QQXKmaXXcow"
token_vk = "e28bf8d579d53aafd83a26361b662b11d1475c810443de2baea4e0fc20a2ae3de0319d1b8f7ed19905e88"

logging.basicConfig(level=logging.INFO)
loop = asyncio.get_event_loop()
bot = Bot(token=token_tg, loop=loop)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

vk = vk_api.VkApi(token=token_vk)
chat_id = 1  # id беседы vk

keyboard = Keyboard()
bot_messages = BotMessages()
manager_photo = ManagerPhoto()

gsheets = GSheets()


def write_msg_vk_bot(message):
    vk.method('messages.send', {'chat_id': chat_id, 'message': message, 'random_id': random.randint(0, 2048)})


@dp.message_handler(commands=['start'], state=None)
async def start_message(message):
    db.create_user_in_db(message.chat.id, message.chat.first_name, message.chat.username)
    db.create_application_in_db(message.chat.id)
    # 0 - Русский, 1 - Английский
    db.add_data_in_applications(message.chat.id, 'language', 0)  # Язык по умлочанию
    await bot.send_message(message.chat.id, bot_messages.start_message(), reply_markup=keyboard.kb_language())
    await User.language.set()


@dp.message_handler(state=User.language)
async def choose_language(message: types.Message, state: FSMContext):
    if message.text in keyboard.language + keyboard.back[db.get_data_from_applications(message.chat.id, 'language')]:
        print(message.text)
        # 0 - Русский, 1 - Английский
        if message.text not in keyboard.back[db.get_data_from_applications(message.chat.id, 'language')]:
            db.add_data_in_applications(message.chat.id, 'language', (0 if message.text == 'Русский' else 1))
        await bot.send_photo(message.chat.id, manager_photo.get_welcome_photo(
            db.get_data_from_applications(message.chat.id, 'language')))
        await bot.send_message(message.chat.id,
                               bot_messages.problems(db.get_data_from_applications(message.chat.id, 'language')),
                               reply_markup=keyboard.kb_problem_area(
                                   db.get_data_from_applications(message.chat.id, 'language')))
        await User.problem_area.set()
    else:
        await bot.send_message(message.chat.id,
                               bot_messages.error(db.get_data_from_applications(message.chat.id, 'language')))
        await User.language.set()


@dp.message_handler(state=User.problem_area)
async def choose_problem_area(message: types.Message, state: FSMContext):
    if message.text in keyboard.problem_area[db.get_data_from_applications(message.chat.id, 'language')]:
        db.add_data_in_applications(message.chat.id, 'problem_area', message.text)
        if message.text in ['Соц. обеспечение', 'Учебный корпус', 'Dormitory', 'Campus']:
            await bot.send_message(message.chat.id, bot_messages.choose_problem(
                db.get_data_from_applications(message.chat.id, 'language')),
                                   reply_markup=keyboard.kb_infrastructure(
                                       db.get_data_from_applications(message.chat.id, 'language')))
            await User.problem.set()
        elif message.text in ['Столовая', 'Cafeteria']:
            await bot.send_message(message.chat.id, bot_messages.choose_problem(
                db.get_data_from_applications(message.chat.id, 'language')),
                                   reply_markup=keyboard.kb_food(
                                       db.get_data_from_applications(message.chat.id, 'language')))
            await User.problem.set()
        elif message.text in ['Другое', 'Other']:
            db.add_data_in_applications(message.chat.id, 'problem', message.text)
            await bot.send_message(message.chat.id,
                                   bot_messages.choose_campus(
                                       db.get_data_from_applications(message.chat.id, 'language')),
                                   reply_markup=keyboard.kb_campuses(
                                       db.get_data_from_applications(message.chat.id, 'language')))
            await User.campus.set()
    elif message.text in keyboard.back[db.get_data_from_applications(message.chat.id, 'language')]:
        await start_message(message)
    else:
        await bot.send_message(message.chat.id,
                               bot_messages.error(db.get_data_from_applications(message.chat.id, 'language')))
        await User.problem_area.set()


@dp.message_handler(state=User.problem)
async def choose_problem(message: types.Message, state: FSMContext):
    if message.text in keyboard.food[db.get_data_from_applications(message.chat.id, 'language')] + \
            keyboard.infrastructure[db.get_data_from_applications(message.chat.id, 'language')]:
        db.add_data_in_applications(message.chat.id, 'problem', message.text)
        await bot.send_message(message.chat.id,
                               bot_messages.choose_campus(db.get_data_from_applications(message.chat.id, 'language')),
                               reply_markup=keyboard.kb_campuses(
                                   db.get_data_from_applications(message.chat.id, 'language')))
        await User.campus.set()
    elif message.text in keyboard.back[db.get_data_from_applications(message.chat.id, 'language')]:
        print("Я нажалась!")
        await choose_language(message, state)
    else:
        await bot.send_message(message.chat.id,
                               bot_messages.error(db.get_data_from_applications(message.chat.id, 'language')))
        await User.problem.set()


@dp.message_handler(state=User.campus)
async def choose_campus(message: types.Message, state: FSMContext):
    if message.text in keyboard.campuses[db.get_data_from_applications(message.chat.id, 'language')]:
        db.add_data_in_applications(message.chat.id, 'campus', message.text)
        await bot.send_photo(message.chat.id, manager_photo.get_tell_problem_photo(
            db.get_data_from_applications(message.chat.id, 'language')))
        await bot.send_message(message.chat.id,
                               bot_messages.tell_problems(db.get_data_from_applications(message.chat.id, 'language')),
                               reply_markup=keyboard.kb_next(
                                   db.get_data_from_applications(message.chat.id, 'language')))
        await User.text_problem.set()
    elif message.text in keyboard.back[db.get_data_from_applications(message.chat.id, 'language')]:
        print("Нажался")
        message.text = db.get_data_from_applications(message.chat.id, 'problem_area')[0]
        await bot.send_message(message.chat.id,
                               bot_messages.problems(db.get_data_from_applications(message.chat.id, 'language')),
                               reply_markup=keyboard.kb_problem_area(
                                   db.get_data_from_applications(message.chat.id, 'language')))
        await User.problem_area.set()
    else:
        await bot.send_message(message.chat.id,
                               bot_messages.error(db.get_data_from_applications(message.chat.id, 'language')))
        await User.campus.set()


@dp.message_handler(state=User.text_problem)
async def bloc_text_problem(message: types.Message, state: FSMContext):
    if message.text not in keyboard.next[db.get_data_from_applications(message.chat.id, 'language')] \
            + keyboard.back[db.get_data_from_applications(message.chat.id, 'language')]:
        print(type(message.text))
        if type(message.text) is str:
            db.add_text_in_applications(message.chat.id, 'text_problem', message.text)
            print(message.text)
        else:
            await bot.send_message(message.chat.id, bot_messages.pls_send_text(
                db.get_data_from_applications(message.chat.id, 'language')))
        await User.text_problem.set()
    elif message.text in keyboard.back[db.get_data_from_applications(message.chat.id, 'language')]:
        message.text = db.get_data_from_applications(message.chat.id, 'problem')
        print(message.text)
        db.clear_cell(message.chat.id, 'applications', 'text_problem')
        await choose_problem(message, state)
    else:
        await bot.send_photo(message.chat.id, manager_photo.get_contact_photo(
            db.get_data_from_applications(message.chat.id, 'language')))
        await bot.send_message(message.chat.id,
                               bot_messages.user_contact(db.get_data_from_applications(message.chat.id, 'language')),
                               reply_markup=keyboard.kb_next(
                                   db.get_data_from_applications(message.chat.id, 'language')))
        await User.contact.set()


@dp.message_handler(state=User.contact)
async def user_contact(message: types.Message, state: FSMContext):
    if message.text not in keyboard.next[db.get_data_from_applications(message.chat.id, 'language')] \
            + keyboard.back[db.get_data_from_applications(message.chat.id, 'language')]:
        if type(message.text) is str:
            db.add_text_in_applications(message.chat.id, 'contact', message.text)
        else:
            await bot.send_message(message.chat.id, bot_messages.pls_send_text(
                db.get_data_from_applications(message.chat.id, 'language')))
        await User.contact.set()
    elif message.text in keyboard.back[db.get_data_from_applications(message.chat.id, 'language')]:
        message.text = db.get_data_from_applications(message.chat.id, 'campus')
        db.clear_cell(message.chat.id, 'applications', 'contact')
        await choose_campus(message, state)
    else:
        await bot.send_photo(message.chat.id,
                             manager_photo.get_bye_photo(db.get_data_from_applications(message.chat.id, 'language')))
        await bot.send_message(message.chat.id,
                               bot_messages.bye(db.get_data_from_applications(message.chat.id, 'language')))

        gsheets.write_user_to_gsheet(db.get_data_from_users(message.chat.id, 'chat_id'),
                                     db.get_data_from_users(message.chat.id, 'name'),
                                     db.get_data_from_users(message.chat.id, 'username'),
                                     db.get_data_from_applications(message.chat.id, 'campus'),
                                     db.get_data_from_applications(message.chat.id, 'problem_area'),
                                     db.get_data_from_applications(message.chat.id, 'problem'),
                                     db.get_data_from_applications(message.chat.id, 'contact'),
                                     db.get_data_from_applications(message.chat.id, 'text_problem'),
                                     db.get_data_from_applications(message.chat.id, 'language'))
        write_msg_vk_bot('Пришла новая заявка №{}\n\n'.format(db.get_count_applications()) +
                         'chat_id: {}\n'.format(db.get_data_from_users(message.chat.id, 'chat_id')) +
                         'username: {}\n'.format(db.get_data_from_users(message.chat.id, 'username')) +
                         'Язык: {}\n'.format('Русский' if db.get_data_from_applications(message.chat.id,
                                                                                        'language') == 0 else 'English') +
                         'Имя: {}\n'.format(db.get_data_from_users(message.chat.id, 'name')) +
                         'Тема заявки: {}\n'.format(db.get_data_from_applications(message.chat.id, 'problem_area')) +
                         'Проблема: {}\n'.format(db.get_data_from_applications(message.chat.id, 'problem')) +
                         'Кампус: {}\n'.format(db.get_data_from_applications(message.chat.id, 'campus')) +
                         'Жалоба: {}\n'.format(db.get_data_from_applications(message.chat.id, 'text_problem')) +
                         'Контактная информация: {}'.format(db.get_data_from_applications(message.chat.id, 'contact'))
                         )

        await state.finish()
        await bot.send_message(message.chat.id,
                               bot_messages.send_start(db.get_data_from_applications(message.chat.id, 'language')),
                               reply_markup=keyboard.kb_start())


executor.start_polling(dp, loop=loop, skip_updates=True)

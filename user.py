from aiogram.dispatcher.filters.state import State, StatesGroup


class User(StatesGroup):
    chat_id = State()
    name = State()
    username = State()
    campus = State()
    problem_area = State()
    problem = State()
    contact = State()
    text_problem = State()
    language = State()

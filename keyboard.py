from telebot import types


class Keyboard:
    def __init__(self):
        self.lang = None  # 0 - Русский, 1 - Английский
        self.problem_area = [['Соц. обеспечение', 'Столовая', 'Учебный корпус', 'Другое'],
                             ['Dormitory', 'Cafeteria', 'Campus', 'Other']]
        self.campuses = [['1', '2', '3'], ['4', '5', '6']]
        self.infrastructure = [['Интернет', 'Некачественное содержание объектов инфраструктуры',
                               'Неудобство пространств', 'Другое'],
                               ['Internet', 'Low-quality infrastructure objects', 'Inconvenience of spaces', 'Other']]
        self.food = [['Неудовлетворительное качество питания', 'Отсутсвие соответствия Заявленным характеристикам блюда',
                     'Неудовлетворительное содержание столовой', 'Другое'],
                     ['Unsatisfactory food quality', 'The dish does not correspond to the declared characteristics',
                      'Poor canteen maintenance', 'Other']]
        self.language = ['Русский', 'English']
        self.back = [['Назад'], ['Back']]
        self.next = [['Далее'], ['Next']]

    def set_language(self, language):
        if language == 'Русский':
            self.lang = 0
        elif language == 'English':
            self.lang = 1

    def kb_problem_area(self):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(*self.problem_area[self.lang])
        keyboard.add(*self.back[self.lang])
        return keyboard

    def kb_campuses(self):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(*self.campuses[self.lang])
        keyboard.add(*self.back[self.lang])
        return keyboard

    def kb_food(self):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(*self.food[self.lang])
        keyboard.add(*self.back[self.lang])
        return keyboard

    def kb_infrastructure(self):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(*self.infrastructure[self.lang])
        keyboard.add(*self.back[self.lang])
        return keyboard

    def kb_language(self):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(*self.language)
        return keyboard

    def kb_next(self):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(*self.next[self.lang])
        keyboard.add(*self.back[self.lang])
        return keyboard

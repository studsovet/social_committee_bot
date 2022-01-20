from aiogram import types


class Keyboard:
    def __init__(self):
        self.problem_area = [['Соц. обеспечение', 'Столовая', 'Учебный корпус', 'Другое'],
                             ['Social security', 'Cafeteria', 'Campus', 'Other']]
        self.campuses = [['Мясницкая 11', 'Мясницкая 20', 'Армянский пер. 4', 'Б. Трёхсвятительский пер. 3',
                          'М. Трехсвятительский пер. 8', 'Покровский бульвар 11', 'Хитровский пер. 2',
                          'Хитровский пер. 4', 'Комплекс зданий «Шаболовка»', 'Ст. Басманная 21', 'Б. Ордынка 47',
                          'М. Ордынка 17', 'Таллинская 34', 'М. Гнездниковский пер. 4', 'М. Пионерская 12',
                          'Потаповский пер 16', 'Профсоюзная 33', 'Славянская площадь 4', 'Трифоновская 57',
                          'Усачева 6', 'Вавилова, 7'],
                         ['Myasnitskaya 11', 'Myasnitskaya 20', 'Armenian per. 4', 'B. Tryokhsvyatitelsky per. 3',
                          'M. Trekhsvyatitelsky per. eight', 'Pokrovsky boulevard 11', 'Khitrovsky per. 2',
                          'Khitrovsky per. 4', 'Complex of buildings "Shabolovka"', 'Art. Basmannaya 21',
                          'B. Ordynka 47', 'M. Ordynka 17', 'Tallinnskaya 34', 'M. Gnezdnikovsky per. 4',
                          'M. Pionerskaya 12', 'Potapovsky lane 16', 'Profsoyuznaya 33', 'Slavyanskaya Square 4',
                          'Trifonovskaya 57', 'Usacheva 6', 'Vavilova, 7']]
        self.infrastructure = [['Интернет', 'Некачественное содержание объектов инфраструктуры',
                                'Неудобство пространств', 'Другое'],
                               ['Internet', 'Low-quality infrastructure objects', 'Inconvenience of spaces', 'Other']]
        self.food = [
            ['Неудовлетворительное качество питания', 'Отсутсвие соответствия Заявленным характеристикам блюда',
             'Неудовлетворительное содержание столовой', 'Другое'],
            ['Unsatisfactory food quality', 'The dish does not correspond to the declared characteristics',
             'Poor canteen maintenance', 'Other']]
        self.language = ['Русский', 'English']
        self.back = [['Назад'], ['Back']]
        self.next = [['Далее'], ['Next']]
        self.start = ['/start']

    def kb_problem_area(self, lang):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(*self.problem_area[lang])
        keyboard.add(*self.back[lang])
        return keyboard

    def kb_campuses(self, lang):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
        keyboard.add(*self.campuses[lang])
        keyboard.add(*self.back[lang])
        return keyboard

    def kb_food(self, lang):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
        keyboard.add(*self.food[lang])
        keyboard.add(*self.back[lang])
        return keyboard

    def kb_infrastructure(self, lang):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
        keyboard.add(*self.infrastructure[lang])
        keyboard.add(*self.back[lang])
        return keyboard

    def kb_language(self):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(*self.language)
        return keyboard

    def kb_next(self, lang):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(*self.next[lang])
        keyboard.add(*self.back[lang])
        return keyboard

    def kb_start(self):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(*self.start)
        return keyboard

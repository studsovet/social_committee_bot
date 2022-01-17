class BotMessages:
    def __init__(self):
        self.lang = None  # 0 - Русский, 1 - Английский
        self.error_message = ['Упсс... Видимо вы ошиблись. Введите корректные данные',
                              'Oops... Looks like you made a mistake. Enter correct data']
        self.welcome_message = 'На каком языке тебе будет удобнее общаться?\nWhich language do you prefer?'
        self.problems_message = ['Привет! Добро пожаловать в форму обратной связи от Социального комитета\n'
                                 'Здесь ты можешь рассказать о проблеме, возникшей в корпусах, общежитиях и '
                                 'столовых. Если проблема другого характера, можно выбрать вариант "Другое".',
                                 'Here you can tell me about a problem you have encountered on campus, '
                                 'in a dormitory or cafeteria.']
        self.choose_problem_message = ['Выбери одну из подкатегорий проблем. '
                                       'Если ты не нашел нужное, выбери "Другое".',
                                       'Choose one of the problem subcategories. '
                                       'If you do not find what you are looking for, select "Other".']
        self.choose_campus_message = ['Выбери свой кампус', 'Choose your campus']
        self.tell_problems_message = ['Расскжи все проблемы, с которыми ты столкнулся.\n'
                                      'Когда закончишь вводить данные напиши "Далее".',
                                      'Tell us all the problems you have encountered.\n'
                                      'When you are done entering the data, write "Next".']
        self.user_contact_message = ['Укажи свои контактные данные, чтобы мы могли с тобой '
                                     'связаться (электронную почту, ссылку на социальные сети). '
                                     'Введи данные одним сообщением\n'
                                     'Если не хочешь оставлять контакты, нажми кнопку "Далее"',
                                     'Enter your contact details so that we can contact you (email, social media link).' 
                                     'Enter data in one message.\n'
                                     'If you do not want to leave contacts, click the "Next" button']
        self.bye_message = ['Скоро мы свяжемся с тобой!',
                            'We will contact you soon!']
        self.pls_send_text_message = ['Пожалуйста отправляйте сообщение текстом.', 'Please send a text message']

    def set_language(self, language):
        if language == 'Русский':
            self.lang = 0
        elif language == 'English':
            self.lang = 1

    def start_message(self):
        return self.welcome_message

    def problems(self):
        return self.problems_message[self.lang]

    def choose_problem(self):
        return self.choose_problem_message[self.lang]

    def choose_campus(self):
        return self.choose_campus_message[self.lang]

    def tell_problems(self):
        return self.tell_problems_message[self.lang]

    def user_contact(self):
        return self.user_contact_message[self.lang]

    def bye(self):
        return self.bye_message[self.lang]

    def error(self):
        return self.error_message[self.lang]

    def pls_send_text(self):
        return self.pls_send_text_message[self.lang]

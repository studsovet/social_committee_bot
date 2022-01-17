class ManagerPhoto:
    def __init__(self):
        self.lang = None
        self.welcome = ['photos/welcome_rus.jpg', 'photos/welcome_eng.jpg']
        self.contact = ['photos/contact_rus.jpg', 'photos/contact_eng.jpg']
        self.tell_problem = ['photos/tell_problem_rus.jpg', 'photos/tell_problem_eng.jpg']
        self.bye = ['photos/bye_rus.jpg', 'photos/bye_eng.jpg']

    def set_language(self, language):
        if language == 'Русский':
            self.lang = 0
        elif language == 'English':
            self.lang = 1

    def get_welcome_photo(self):
        return open(self.welcome[self.lang], 'rb')

    def get_contact_photo(self):
        return open(self.contact[self.lang], 'rb')

    def get_tell_problem_photo(self):
        return open(self.tell_problem[self.lang], 'rb')

    def get_bye_photo(self):
        return open(self.bye[self.lang], 'rb')

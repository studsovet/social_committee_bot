class ManagerPhoto:
    def __init__(self):
        self.welcome = ['photos/welcome_rus.jpg', 'photos/welcome_eng.jpg']
        self.contact = ['photos/contact_rus.jpg', 'photos/contact_eng.jpg']
        self.tell_problem = ['photos/tell_problem_rus.jpg', 'photos/tell_problem_eng.jpg']
        self.bye = ['photos/bye_rus.jpg', 'photos/bye_eng.jpg']

    def get_welcome_photo(self, lang):
        return open(self.welcome[lang], 'rb')

    def get_contact_photo(self, lang):
        return open(self.contact[lang], 'rb')

    def get_tell_problem_photo(self, lang):
        return open(self.tell_problem[lang], 'rb')

    def get_bye_photo(self, lang):
        return open(self.bye[lang], 'rb')

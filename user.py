class User:
    def __init__(self, chat_id, name, username):
        self.chat_id = chat_id
        self.name = name
        self.username = username
        self.campus = None
        self.problem_area = None
        self.problem = None
        self.contact = ""
        self.text_problem = ""
        self.language = None

    def add_campus(self, campus):
        self.campus = campus

    def add_problem_area(self, problem_area):
        self.problem_area = problem_area

    def add_problem(self, problem):
        self.problem = problem

    def add_contact(self, contact):
        self.contact += contact

    def add_text_problem(self, text_problem):
        self.text_problem += text_problem

    def add_language(self, language):
        self.language = language

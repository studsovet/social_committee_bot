import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials

# Файл, полученный в Google Developer Console
import db

CREDENTIALS_FILE = "creds.json"
# ID Google Sheets документа (взят из URL)
spreadsheet_id = "17StUoAAB_5KP77grySt4n62B52K7QRGJnrwYUBD-dU0"


# Авторизуемся и получаем service — экземпляр доступа к API
def auth_gsheet():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"])
    httpAuth = credentials.authorize(httplib2.Http())
    return apiclient.discovery.build("sheets", "v4", http=httpAuth)


class GSheets:
    def __init__(self):
        self.service = auth_gsheet()

    def write_user_to_gsheet(self, chat_id, name, username, campus, problem_area, problem, contact, text_problem,
                             language):
        count_applications = self.get_count_applications()
        values = self.service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {"range": "A{}:J{}".format(count_applications + 2, count_applications + 2),
                     "majorDimension": "ROWS",
                     "values": [
                         [chat_id, name, username, campus, problem_area, problem, contact, text_problem, language,
                          db.get_time_application(chat_id)]]},
                ]
            }
        ).execute()
        self.write_count_applications(count_applications + 1)

    def get_count_applications(self):
        val = self.service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range='L1',
            majorDimension='ROWS'
        ).execute()
        return int(val['values'][0][0])

    def write_count_applications(self, count):
        val = self.service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {"range": "L1",
                     "majorDimension": "ROWS",
                     "values": [[count]]}
                ]
            }
        ).execute()

    def get_cell(self, cell):
        val = self.service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=cell,
            majorDimension='ROWS'
        ).execute()
        return val['values'][0][0]

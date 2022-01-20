import httplib2
import apiclient
import db
from oauth2client.service_account import ServiceAccountCredentials

# Файл, полученный в Google Developer Console
CREDENTIALS_FILE = "creds.json"
# ID Google Sheets документа (взят из URL)
spreadsheet_id = "17StUoAAB_5KP77grySt4n62B52K7QRGJnrwYUBD-dU0"


# class MemoryCache(Cache):
#     _CACHE = {}
#
#     def get(self, url):
#         return MemoryCache._CACHE.get(url)
#
#     def set(self, url, content):
#         MemoryCache._CACHE[url] = content


# Авторизуемся и получаем service — экземпляр доступа к API
def auth_gsheet():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"])
    httpAuth = credentials.authorize(httplib2.Http())
    return apiclient.discovery.build("sheets", "v4", http=httpAuth, cache_discovery=False)


class GSheets:
    def __init__(self):
        self.service = auth_gsheet()

    def write_user_to_gsheet(self, chat_id, name, username, campus, problem_area, problem, contact, text_problem,
                             language):
        values = self.service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {"range": "A{}:I{}".format(db.get_count_applications() + 1, db.get_count_applications() + 1),
                     "majorDimension": "ROWS",
                     "values": [
                         [chat_id, name, username, campus, problem_area, problem, contact, text_problem, language]]},
                ]
            }
        ).execute()
        self.write_count_applications(db.get_count_applications())

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

import gspread_asyncio
from core.config import Config
from oauth2client.service_account import ServiceAccountCredentials
from core.exceptions import ForbiddenError, NotAcceptableError, NotFoundError, ValidationError
from gspread.exceptions import SpreadsheetNotFound, NoValidUrlKeyFound


class GoogleSheetService:
    @staticmethod
    def _get_credentials():
        credentials = Config.GOOGLE_SHEETS_DATA
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            credentials,
            scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"])  # type: ignore
        return credentials

    async def fetch_by_url(self, spreadsheet_url: str):
        gc = gspread_asyncio.AsyncioGspreadClientManager(self._get_credentials)
        gc = await gc.authorize()

        try:
            spreadsheet = await gc.open_by_url(spreadsheet_url)
        except PermissionError:
            raise ForbiddenError(detail="Access to the spreadsheet forbidden")
        except NoValidUrlKeyFound:
            raise ValidationError('Invalid spreadsheet url')
        except SpreadsheetNotFound:
            raise NotFoundError(detail="Spreadsheet is not found")

        spreadsheet = await spreadsheet.get_sheet1()
        data = await spreadsheet.get_all_values()

        if data == [[]]:
            raise NotAcceptableError(detail="Spreadsheet is empty")

        table_header = [cell.lower() for cell in data[0]]
        if not {"email", "score"}.issubset(set(table_header)):
            raise NotAcceptableError(detail="Some of columns not found")

        data = [dict(zip(table_header, row)) for row in data[1:]]
        return data

    async def create_table(self, olymp_title: str, teams: list[dict]) -> str:
        olymp_title = f"Распределение участников олимпиады {olymp_title}"

        gc = gspread_asyncio.AsyncioGspreadClientManager(self._get_credentials)
        gc = await gc.authorize()

        spreadsheet = await gc.create(title=olymp_title)
        await gc.insert_permission(spreadsheet.id, None, perm_type="anyone", role="writer")

        sheet = await spreadsheet.get_sheet1()
        await sheet.delete_rows(2, 1000)
        await sheet.delete_columns(4, 26)

        await sheet.append_row(["Команда", "ФИО", "Email", "Специализация"])
        print(teams)
        for team in teams:
            row_start = sheet.row_count
            members = [
                [team['title'], member['fullname'], member['email'], member['profession']] for member in
                team['members']
            ]
            await sheet.append_rows(members)
            row_end = sheet.row_count
            await sheet.merge_cells(f"A{row_start}:A{row_end}")

        await sheet.columns_auto_resize(1, 3)
        return spreadsheet.url

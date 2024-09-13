import logging
import os
from abc import abstractmethod
from datetime import datetime

import pandas as pd
from gspread_dataframe import set_with_dataframe

from b_moz.libs.io.google import GoogleSpreadSheet


class ResultExporter:
    def __init__(self, filename: str = ""):
        self._logger = logging.getLogger(__name__)
        if filename is not None and filename != "":
            self._filename = filename
        else:
            self._filename = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def filename(self) -> str:
        if self._filename is not None and self.filename != "":
            return self._filename
        return f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    @abstractmethod
    def export(self, data: pd.DataFrame, **kwargs) -> str:
        pass


class LocalCSVExporter(ResultExporter):
    def __init__(self, filename: str = "", path: str = ""):
        super().__init__(filename=filename)
        if path:
            from b_moz.libs.project import temp_path

            self.path = temp_path()
        else:
            self.path = path

    def export(self, data: pd.DataFrame, **kwargs) -> str:
        _file_name = self.filename()
        os.chdir(self.path)
        data.to_csv(
            _file_name,
            header=True,
            index=False,
            encoding="utf-8",
            lineterminator="\r\n",
        )
        return os.path.abspath(_file_name)


class GoogleSpreadSheetExporter(ResultExporter):
    def __init__(self, filename: str = "", file_id: str = ""):
        super().__init__(filename=filename)
        self._file_id = file_id
        self._client = GoogleSpreadSheet.get_client()
        if not self._file_id:
            raise ValueError("File ID is not set.")
        self._workbook = self._client.open_by_key(self._file_id)

    def export(
        self,
        data: pd.DataFrame,
        sheet_name: str = "data",
        clear_sheet: bool = False,
        **kwargs,
    ) -> str:
        """Export data to Google Spread Sheet."""

        sheet = None
        include_column_header = False
        for s in self._workbook.worksheets():  # to handle sheet is not in the workbook
            if s.title == sheet_name:
                sheet = s
                break
        if not sheet:
            sheet = self._workbook.add_worksheet(title=sheet_name, rows=1, cols=1)
            include_column_header = True
            row = 1
        else:
            last_row = len(sheet.get_all_values())
            row = last_row + 1

        if clear_sheet:
            sheet.clear()
            set_with_dataframe(sheet, data)
        else:
            set_with_dataframe(
                sheet,
                data,
                row=row,
                col=1,
                include_index=False,
                include_column_header=include_column_header,
            )
        return f"https://docs.google.com/spreadsheets/d/{self._file_id}/"

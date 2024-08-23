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

    def export(
        self,
        data: pd.DataFrame,
        sheet_name: str = "data",
        clear_sheet: bool = False,
        **kwargs,
    ) -> str:
        """Export data to Google Spread Sheet."""
        if not self._file_id:
            raise ValueError("File ID is not set.")
        client = GoogleSpreadSheet.get_client()
        sheet = client.open_by_key(self._file_id).worksheet(sheet_name)
        if clear_sheet:
            sheet.clear()
            set_with_dataframe(sheet, data)
        else:
            last_row = len(sheet.get_all_values())
            set_with_dataframe(
                sheet,
                data,
                row=last_row + 1,
                col=1,
                include_index=False,
                include_column_header=False,
            )
        return f"https://docs.google.com/spreadsheets/d/{self._file_id}/"

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QDate

class ReadData:
    def __init__(self, dialog):
        self.dialog = dialog

    def get_dates(self):
        # Reads the dates from the interface and validates them.
        start_qdate = self.dialog.start_date.date()
        end_qdate = self.dialog.end_date.date()

        if start_qdate > end_qdate:
            QMessageBox.warning(
                self.dialog,
                "Date Error",
                "The start date cannot be after the end date."
            )
            return None

        start_date = start_qdate.toString("yyyy-MM-dd")
        end_date = end_qdate.toString("yyyy-MM-dd")

        return start_date, end_date

    def show_selected_dates(self, start_date, end_date):
        # Displays a QMessageBox with the selected dates.
        QMessageBox.information(
            self.dialog,
            "Selected Dates",
            f"Start date: {start_date}\nEnd date: {end_date}"
        )

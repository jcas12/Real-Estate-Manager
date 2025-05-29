from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from BackendSection.DBConnection import DBConnection

# This class handles the window that displays a report of all houses in a table
class ListHouseWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("UiFolder/Report.ui", self)  # Load the UI layout for the report window
        self.load_data()  # Load data into the table when the window opens

    def load_data(self):
        database = DBConnection()  # Connect to the database
        results = database.select_all_houses()  # Get all house records

        # Prepare the table: clear it and set the correct number of rows and columns
        self.houses_tableWidget.setRowCount(0)
        self.houses_tableWidget.setRowCount(len(results))
        self.houses_tableWidget.setColumnCount(9)  # There are 10 columns in the DB, but we skip the photo (index 7)

        # Set the column headers for the table
        headers = [
            "ID", "Address 1", "Address 2", "City", "State",
            "Postal Code", "Country", "Size (m²)", "Register Date"
        ]
        self.houses_tableWidget.setHorizontalHeaderLabels(headers)

        # Loop through the house data and fill the table
        for row_index, row_data in enumerate(results):
            col = 0
            for i, value in enumerate(row_data):
                if i == 7:  # Skip the 'photo' column (index 7), we don't display it
                    continue
                # Set each cell in the table with the value from the database
                self.houses_tableWidget.setItem(row_index, col, QTableWidgetItem(str(value)))
                col += 1

        database.close()  # Close the database connection after loading the data
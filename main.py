import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication, QInputDialog, QMessageBox
from PyQt5.QtGui import QIcon
from BackendSection.AddHouse import AddHouseWidget
from BackendSection.ModifyHouse import ModifyHouseWidget
from BackendSection.ViewHouse import ViewHouseWidget
from BackendSection.ListHouse import ListHouseWidget
from BackendSection.DBConnection import DBConnection
from BackendSection.RemoveHouse import RemoveHouseWidget

# This is the main window of the app
class MainWindow(QMainWindow):
    def __init__(self):
        self.app = QApplication(sys.argv)  # Starts the Qt application
        super().__init__()
        self.window = loadUi("UiFolder/MainWindow.ui", self)  # Loads the UI design of the main window
        self.setWindowIcon(QIcon("icons/mainwindowhouse.png"))
        # Create instances of other windows/widgets used in the app
        self.listHouses = ListHouseWidget()  # The screen that shows all houses in a table
        self.addHouse = AddHouseWidget(report_widget=self.listHouses)  # The form to add a new house

        # Connect the menu buttons to their corresponding functions
        self.actionAddHouse.triggered.connect(self.show_add_house)
        self.actionModifyHouse.triggered.connect(self.modify_house)
        self.actionSearchHouse.triggered.connect(self.view_house)
        self.actionReport.triggered.connect(self.listHouses.show)
        self.actionExit.triggered.connect(self.quitApp)
        self.actionHelpContents.triggered.connect(self.show_help)
        self.actionAbout.triggered.connect(self.show_about)
        self.actionRemoveHouse.triggered.connect(self.open_remove_house)
        self.window.show()  # Shows the main window

    # Show the add house form
    def show_add_house(self):
        self.addHouse.reset_form()  # Resets the form (like generating a new ID)
        self.addHouse.show()  # Opens the add house window

    # Close the entire app
    def quitApp(self):
        sys.exit(0)

    # Opens the view-only window for a specific house based on ID
    def view_house(self):
        id_str, ok = QInputDialog.getText(self, "Search House", "Enter House ID:")  # Ask user for house ID
        if ok and id_str:
            db = DBConnection()  # Connect to the database
            house = db.select_by_id(id_str)  # Search for a house with that ID

            if house:
                self.viewHouse = ViewHouseWidget(id_str)  # If found, open the view window
                self.viewHouse.show()
            else:
                QMessageBox.warning(self, "Error", "No house found with the entered ID.")
                db.close()

    # Opens the modify window for a house based on ID
    def modify_house(self):
        id, ok = QInputDialog.getText(self, "Modify House", "Enter House ID:")  # Ask user for house ID
        if ok and id:
            self.modifyHouse = ModifyHouseWidget(id, self.listHouses)  # Try to load the modify window
        if self.modifyHouse.valid:  # Only show the window if the house exists
            self.modifyHouse.show()  
    
    # Opens the remove window based on IUD
    def open_remove_house(self):
        RemoveHouseWidget(report_widget=self.listHouses)

    # Show instructions/help text
    def show_help(self):
        help_text = (
            "Welcome to the Real State Manager!\n\n"
            "Here is how you can use each option:\n\n"
            "* Add House: Opens a form to add a new house with all its details and photo.\n"
            "* Modify House: Enter a House ID to edit its information.\n"
            "* Search for a House: Enter a House ID to view its details and image.\n"
            "* Report: Displays a table with all houses (without images).\n"
            "* Help: Shows this window.\n"
            "* About: Shows developer team information.\n\n"
            "Make sure to fill all required fields!"
        )
        QMessageBox.information(self, "Help", help_text)

    # Show credits/about info
    def show_about(self):
        QMessageBox.information(self, "About", "Developed by: Argenis, Juan & Julio")

# Starts the app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

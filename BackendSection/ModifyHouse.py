from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from BackendSection.House import House
from BackendSection.DBConnection import DBConnection

# This class manages the window for modifying an existing house
class ModifyHouseWidget(QWidget):
    def __init__(self, house_id, report_widget=None):
        super().__init__()
        loadUi("UiFolder/ModifyHouse.ui", self)  # Load the window design from the .ui file
        self.report_widget = report_widget  # Optional: the report table to refresh after saving
        self.house_id = house_id  # The ID of the house to be modified
        self.database = DBConnection()  # Connect to the database
        self.photo_path = ""  # Path to the house photo (if any)
        self.valid = False  # Used to check if the house was successfully loaded

        # Connect buttons to their actions
        self.modify_pushButton.clicked.connect(self.modify_clicked)  # Modify button
        self.modify_cancelButton.clicked.connect(self.close)  # Cancel button
        self.modify_photoButton.clicked.connect(self.browse_photo)  # Browse photo button

        self.load_data()  # Load the house data into the form

    def load_data(self):
        # Try to find the house with the given ID
        house = self.database.select_by_id(self.house_id)
        if house:
            self.valid = True  # The house exists and was loaded

            # Fill the form with house data
            self.id_lineEdit.setText(house.get_id())
            self.id_lineEdit.setReadOnly(True)
            self.address1_lineEdit.setText(house.get_address1())
            self.address2_lineEdit.setText(house.get_address2())
            self.city_lineEdit.setText(house.get_city())
            self.state_lineEdit.setText(house.get_state())
            self.postalcode_lineEdit.setText(house.get_postal_code())
            self.country_lineEdit.setText(house.get_country())
            self.size_lineEdit.setText(str(house.get_size()))
            self.date_dateEdit.setDate(house.get_register_date())

            # Show the house photo (if available)
            self.photo_path = house.get_photo_path()
            if self.photo_path:
                self.photo_label.setPixmap(QPixmap(self.photo_path).scaled(200, 200))
            else:
                self.photo_label.setText("No Photo")
        else:
            # If house is not found, show error and close window
            QMessageBox.critical(self, "Error", f"No house found with ID {self.house_id}")
            self.valid = False
            self.close()
            return

    def browse_photo(self):
        # Let user pick an image file
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Photo", "", "Images (*.png *.jpg *.jpeg)")
        if file_name:
            self.photo_path = file_name  # Save path of selected image
            self.photo_label.setPixmap(QPixmap(file_name).scaled(200, 200))  # Show image in UI

    def modify_clicked(self):
        # Get the updated values from the form
        address1 = self.address1_lineEdit.text().strip()
        address2 = self.address2_lineEdit.text().strip()
        city = self.city_lineEdit.text().strip()
        state = self.state_lineEdit.text().strip()
        postal_code = self.postalcode_lineEdit.text().strip()
        country = self.country_lineEdit.text().strip()
        size_text = self.size_lineEdit.text().strip()

        # Validate required fields (Address2 and photo are optional)
        if not all([address1, city, state, postal_code, country, size_text]):
            QMessageBox.warning(self, "Error", "All fields except Address 2 and Photo are required.")
            return

        # Address 1 must have at least 8 characters and not be only digits
        if len(address1) < 8 or address1.isdigit():
            QMessageBox.warning(self, "Error", "Address 1 must be at least 8 characters.")
            return

        # State must be 2 letters (e.g. NY, PR)
        if len(state) != 2 or not state.isalpha():
            QMessageBox.warning(self, "Error", "State must be two letters (e.g., PR, NY).")
            return

        # Postal code must be exactly 5 digits
        if not postal_code.isdigit() or len(postal_code) != 5:
            QMessageBox.warning(self, "Error", "Postal Code must be 5 digits.")
            return

        # Convert size to float and check it’s a positive number
        try:
            size = float(size_text.replace(",", "."))
            if size <= 0:
                raise ValueError()
        except ValueError:
            QMessageBox.warning(self, "Error", "Size must be a positive number.")
            return

        # Create a new House object with the updated data
        house = House(
            self.house_id,
            address1, address2, city, state,
            postal_code, country,
            self.photo_path,
            size,
            self.date_dateEdit.date().toPyDate()
        )

        # Update the house in the database
        rows = self.database.update(house)
        if rows > 0:
            QMessageBox.information(self, "Success", f"House modified successfully.")

            # If there is a report table, refresh it
            try:
                if self.report_widget:
                    self.report_widget.load_data()
            except Exception as e:
                print(e)

            self.close()  # Close the modify window after success
        else:
            QMessageBox.critical(self, "Error", "Failed to modify house.")
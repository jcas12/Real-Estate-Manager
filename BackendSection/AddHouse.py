from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from BackendSection.House import House
from BackendSection.DBConnection import DBConnection

# This class handles the "Add House" window
class AddHouseWidget(QWidget):
    def __init__(self, report_widget=None):  
        super().__init__()
        loadUi("UiFolder/AddHouse.ui", self)  # Loads the user interface from the .ui file
        self.report_widget = report_widget  # Optional: a report table widget to refresh after adding a house
        self.database = DBConnection()  # Connect to the database
        self.photo_path = ""  # Stores the selected photo path

        # Connect buttons to functions
        self.add_push_button.clicked.connect(self.add_house_clicked)  # When the user clicks "Add", run add_house_clicked
        self.photo_button.clicked.connect(self.browse_photo)  # When user clicks "Photo", run browse_photo

        self.reset_form()  # Reset all input fields when the form loads

    def reset_form(self):
        # Get the next available ID from the database and set it (read-only)
        new_id = self.database.get_next_id()
        self.id_lineEdit.setText(new_id)
        self.id_lineEdit.setReadOnly(True)

        # Clear all the input fields
        self.address1_lineEdit.clear()
        self.address2_lineEdit.clear()
        self.city_lineEdit.clear()
        self.state_lineEdit.clear()
        self.postalcode_lineEdit.clear()
        self.country_lineEdit.clear()
        self.size_lineEdit.clear()
        self.date_dateEdit.setDate(self.date_dateEdit.minimumDate())  # Reset date to minimum

        # Reset photo area
        self.photo_label.setText("No Photo")
        self.photo_label.setPixmap(QPixmap())
        self.photo_path = ""

    def browse_photo(self):
        # Open file dialog for user to choose a photo
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Photo", "", "Images (*.png *.jpg *.jpeg)")
        if file_name:
            self.photo_path = file_name  # Save the file path
            self.photo_label.setPixmap(QPixmap(file_name).scaled(200, 200))  # Display the image scaled

    def add_house_clicked(self):
        # Get all the input values from the form
        house_id = self.id_lineEdit.text().strip()
        address1 = self.address1_lineEdit.text().strip()
        address2 = self.address2_lineEdit.text().strip()
        city = self.city_lineEdit.text().strip()
        state = self.state_lineEdit.text().strip()
        postal_code = self.postalcode_lineEdit.text().strip()
        country = self.country_lineEdit.text().strip()
        size_text = self.size_lineEdit.text().strip()

        # Validate that required fields are filled (Address2 and Photo are optional)
        if not all([address1, city, state, postal_code, country, size_text]):
            QMessageBox.warning(self, "Error", "All fields except Address 2 and Photo are required.")
            return

        # Validate Address 1 (at least 8 characters and not only numbers)
        if len(address1) < 8 or address1.isdigit():
            QMessageBox.warning(self, "Error", "Address 1 must be at least 8 characters.")
            return

        # Validate city (at least 2 letters, no numbers)
        if len(city) < 2 or not city.replace(" ", "").isalpha():
            QMessageBox.warning(self, "Error", "City must be at least 2 letters.")
            return

        # Validate country (at least 2 letters, no numbers)
        if len(country) < 2 or not country.replace(" ", "").isalpha():
            QMessageBox.warning(self, "Error", "Country must be at least 2 letters.")
            return

        # Validate state (must be exactly 2 letters, like PR or NY)
        if len(state) != 2 or not state.isalpha():
            QMessageBox.warning(self, "Error", "State must be two letters (e.g., PR, NY).")
            return

        # Validate postal code (must be 5 digits)
        if not postal_code.isdigit() or len(postal_code) != 5:
            QMessageBox.warning(self, "Error", "Postal Code must be 5 digits.")
            return

        # Validate size (must be a positive number)
        try:
            size = float(size_text)
            if size <= 0:
                raise ValueError()
        except ValueError:
            QMessageBox.warning(self, "Error", "Size must be a positive number.")
            return

        # Check if a house with this ID already exists
        if self.database.select_by_id(house_id):
            QMessageBox.warning(self, "Error", "A house with this ID already exists.")
            return

        # Create a new House object with the data from the form
        house = House(
            house_id,
            address1, address2, city, state,
            postal_code, country,
            getattr(self, 'photo_path', ""),
            size,
            self.date_dateEdit.date().toPyDate()
        )

        # Try to add the house to the database
        rows, inserted_id = self.database.add(house)
        if rows > 0:
            QMessageBox.information(self, "Success", f"House saved with ID {inserted_id}")
            try:
                if self.report_widget:
                    self.report_widget.load_data()  # Refresh the report table if available
            except Exception as e:
                print(e)
            self.close()  # Close the add form after saving
        else:
            QMessageBox.critical(self, "Error", "Failed to save house.")
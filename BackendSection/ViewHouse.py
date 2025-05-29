from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap
from BackendSection.DBConnection import DBConnection

class ViewHouseWidget(QMainWindow):
    def __init__(self, house_id):
        super().__init__()
        loadUi("UiFolder/SearchHouse.ui", self)
        self.search_cancel_button.clicked.connect(self.close)
        self.house_id = house_id
        self.load_data()

    def load_data(self):
        database = DBConnection()
        house = database.select_by_id(self.house_id)

        if house:
            self.id_lineEdit.setText(house.get_id())
            self.address1_lineEdit.setText(house.get_address1())
            self.address2_lineEdit.setText(house.get_address2())
            self.city_lineEdit.setText(house.get_city())
            self.state_lineEdit.setText(house.get_state())
            self.postal_lineEdit.setText(house.get_postal_code())
            self.country_lineEdit.setText(house.get_country())
            self.size_lineEdit.setText(str(house.get_size()))
            self.date_dateEdit.setDate(house.get_register_date())

            photo_path = house.get_photo_path()
            if photo_path:
                pixmap = QPixmap(photo_path).scaled(150, 150)
                self.photo_label.setPixmap(pixmap)
        else:
            print(f"No house found with ID {self.house_id}")

        database.close()
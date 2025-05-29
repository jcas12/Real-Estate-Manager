from PyQt5.QtWidgets import QWidget, QMessageBox, QInputDialog
from PyQt5.QtGui import QIcon
from BackendSection.DBConnection import DBConnection

class RemoveHouseWidget(QWidget):
    def __init__(self, report_widget=None):
        super().__init__()
        self.database = DBConnection()
        self.report_widget = report_widget
        self.prompt_and_remove()
    def prompt_and_remove(self):
        house_id, ok = QInputDialog.getText(self, "Remove House", "Enter the House ID to remove:")

        if not ok or not house_id.strip():
            return  # User cancelled or entered nothing

        house_id = house_id.strip()
        house = self.database.select_by_id(house_id)

        if not house:
            QMessageBox.warning(self, "House Not Found", f"No house found with ID '{house_id}'.")
            return

        confirm = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete the house with ID '{house_id}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            if self.database.delete(house_id):
                QMessageBox.information(self, "Deleted", f"The house with ID '{house_id}' has been deleted.")

                # Refresh report widget if provided
                try:
                    if self.report_widget:
                        self.report_widget.load_data()
                except Exception as e:
                    print(e)
            else:
                QMessageBox.warning(self, "Error", "Something went wrong while deleting.")
        else:
            QMessageBox.information(self, "Cancelled", "Deletion cancelled.")
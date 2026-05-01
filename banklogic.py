import csv
import time

from bankui import *
from PyQt6.QtWidgets import *


class Banklogic(QMainWindow, Ui_MainWindow):
    account_id = 0

    def __init__(self, id, login_window) -> None:
        """Initializes the bank window for the given account ID and loads existing data."""
        super().__init__()
        self.setupUi(self)
        self.account_id = id
        self.login_window = login_window

        self.DepositButton.clicked.connect(lambda: self.deposit())
        self.WidthdrawButton.clicked.connect(lambda: self.withdraw())
        self.SaveButton.clicked.connect(lambda: self.submit())
        self.load_data()
        self.AccountNumberText.setText(str(id))

    def load_data(self) -> None:
        """Loads previously saved account data for the current account from the CSV file."""
        try:
            with open("bankdata.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and int(row[0]) == self.account_id:
                        self.FirstNameField.setText(row[1])
                        self.LastNameField.setText(row[2])
                        self.DobDate.setDate(
                            QtCore.QDate.fromString(row[3], "MM/dd/yyyy")
                        )
                        self.SsnField.setText(row[4])
                        self.AccountNumberText_2.setText(row[5])
                        self.TransactionText.setText(row[6])
                        index = self.comboBox.findText(
                            row[7]
                        )  # I did look this up aswell
                        if index >= 0:
                            self.comboBox.setCurrentIndex(index)
        except FileNotFoundError:
            pass

    def deposit(self) -> None:
        """Adds the entered amount to the current balance and updates the last transaction date."""
        amount = self.DepositField.text().strip()
        try:
            amount = float(amount)
        except ValueError:
            self.ErrorLabel.setText("Invalid deposit amount")
            return

        current = float(self.AccountNumberText_2.text().replace("$", "").strip())
        new_balance = current + amount
        self.AccountNumberText_2.setText(f"${new_balance:.2f}")
        self.TransactionText.setText(QtCore.QDate.currentDate().toString("MM/dd/yyyy"))
        self.DepositField.clear()
        self.ErrorLabel.setText(f"Successfully deposited ${amount:.2f}")

    def withdraw(self) -> None:
        """Subtracts the entered amount from the balance, Does overdraw protection if enabled."""
        amount = self.WidthdrawField.text().strip()
        try:
            amount = float(amount)
        except ValueError:
            self.ErrorLabel.setText("Invalid withdrawal amount")
            return

        current = float(self.AccountNumberText_2.text().replace("$", "").strip())
        overdraw_protection = self.comboBox.currentText() == "Yes"

        if amount > current and overdraw_protection:
            self.ErrorLabel.setText("Insufficient funds")
            return

        new_balance = current - amount
        self.AccountNumberText_2.setText(f"${new_balance:.2f}")
        self.TransactionText.setText(QtCore.QDate.currentDate().toString("MM/dd/yyyy"))
        self.WidthdrawField.clear()
        self.ErrorLabel.setText(f"Successfully withdrew ${amount:.2f}")

    def submit(self) -> None:
        """Saves all account data to the CSV file and returns to the login window."""
        first = self.FirstNameField.text().strip()
        last = self.LastNameField.text().strip()
        dob = self.DobDate.text().strip()
        ssn = self.SsnField.text().strip()
        balance = self.AccountNumberText_2.text().strip()
        last_transaction = self.TransactionText.text().strip()
        overdraw = self.comboBox.currentText()
        id = self.account_id

        rows = []
        account_found = False

        try:
            with open("bankdata.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and int(row[0]) == id:
                        rows.append(
                            [  # My IDE does auto formatting so it does this when lines get long
                                id,
                                first,
                                last,
                                dob,
                                ssn,
                                balance,
                                last_transaction,
                                overdraw,
                            ]
                        )
                        account_found = True
                    else:
                        rows.append(row)
        except FileNotFoundError:
            pass

        if not account_found:
            rows.append(
                [id, first, last, dob, ssn, balance, last_transaction, overdraw]
            )

        with open("bankdata.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        self.ErrorLabel.setText("Saving...")
        QApplication.processEvents()
        time.sleep(2)
        self.login_window.show()
        self.close()

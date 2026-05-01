import csv
import time  # Didnt cover in class but I was aware of it before hand and looked up how to use sleep.

from banklogic import *
from bankloginui import *
from PyQt6.QtWidgets import *


class Bankloginlogic(QMainWindow, Ui_MainBankWindow):
    def __init__(self) -> None:
        """Initializes the bank login window and connects the login button."""
        super().__init__()
        self.setupUi(self)

        self.LoginButton.clicked.connect(lambda: self.submit())

    def submit(self) -> None:
        """Validates the entered account number and password, then logs in or creates a new account."""
        id = self.AcountField.text().strip()
        password = self.PasswordField.text().strip()

        if not id:
            self.StatusLabel.setText("No account number entered")
            return
        elif id:
            try:
                id = int(id)
            except ValueError:
                self.StatusLabel.setText("Account number must consit of only numbers")
                return
            else:
                if not password:
                    self.StatusLabel.setText("No password entered")
                    return

        try:
            with open("Bankaccounts.csv", "r") as accounts:
                pass
        except FileNotFoundError:
            with open("Bankaccounts.csv", "w", newline="") as csv_file:
                pass

        with open("Bankaccounts.csv", "r") as accounts:
            account_found = False
            password_test = ""
            for line in accounts:
                line = line.strip().split(",")
                if int(line[0]) == id:
                    account_found = True
                    password_test = line[1]
            if account_found:
                if password == password_test:
                    self.StatusLabel.setText("Successfully logged in!")
                    QApplication.processEvents()  # I used google to find this, I had the problem that the label wasnt getting updated before the sleep happened. This just forces it to load.
                    self.open_account(id)
                    return
                else:
                    self.StatusLabel.setText("Incorrect password(Case sensitive)")
                    return
            else:
                self.StatusLabel.setText("Account not found, creating new one...")
                QApplication.processEvents()  # I used google to find this, I had the problem that the label wasnt getting updated before the sleep happened. This just forces it to load.
                self.create_account(id, password)
                return

    def create_account(self, id, password) -> None:
        """Creates a new bank account and writes it to the CSV file."""
        with open("bankaccounts.csv", "a", newline="") as accounts:
            content = csv.writer(accounts)
            content.writerow([id, password])
        self.open_account(id)

    def open_account(self, id) -> None:
        """Opens the bank window for the given account ID and closes the login window."""
        time.sleep(2)
        self.bank_window = Banklogic(
            id, self
        )  # For this and the next line I did use AI to help me figure out how to utilize two windows without producing the "QCoreApplication::exec: The event loop is already running" error.
        self.bank_window.show()
        self.AcountField.clear()
        self.PasswordField.clear()
        self.StatusLabel.setText("Please enter your bank details")
        self.close()

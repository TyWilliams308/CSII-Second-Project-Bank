from bankloginlogic import *
from PyQt6.QtWidgets import QApplication


def main() -> None:
    application = QApplication([])
    window = Bankloginlogic()
    window.show()
    application.exec()


if __name__ == "__main__":
    main()

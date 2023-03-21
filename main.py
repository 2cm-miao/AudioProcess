import sys

import interface
from PyQt5.QtWidgets import (QApplication)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = interface.WindowFunction()
    player.show()
    sys.exit(app.exec_())

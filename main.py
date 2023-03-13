# This is a sample Python script.
import sys

import interface
from PyQt5.QtWidgets import (QApplication)


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.




def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = interface.WindowFunction()
    player.resize(640, 480)
    player.show()
    sys.exit(app.exec_())



# See PyCharm help at https://www.jetbrains.com/help/pycharm/

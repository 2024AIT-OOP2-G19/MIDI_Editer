import dawdreamer

import PySide6
from PySide6.QtWidgets import (QApplication, QWidget)

class TestWindow(QWidget):              # ウィンドウ系クラスを継承すること
    def __init__(self, parent=None):    # parentは他にウィンドウを表示させる場合に指定する
        super().__init__(parent)        # 継承元クラス（ここではQWidget）を初期化

        self.setWindowTitle('vstTest')


if __name__ == "__main__":
    app = QApplication()
    window = TestWindow()
    window.show()
    app.exec()

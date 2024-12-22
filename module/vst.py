import dawdreamer

from PySide6.QtWidgets import (QApplication, QWidget, QPushButton)
'''
テスト用クラス
'''
class TestWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('vstTest')
        self.resize(200, 110)

        load_vst_btn = QPushButton(self)
        load_vst_btn.move(20, 10)
        load_vst_btn.setText('load vst')
        # load_vst_btn.pressed.connect()

        vst_option_btn = QPushButton(self)
        vst_option_btn.move(20, 40)
        vst_option_btn.setText('vst option')
        # vst_option_btn.pressed.connect()

        render_btn = QPushButton(self)
        render_btn.move(20, 70)
        render_btn.setText('render')
        # render_btn.pressed.connect()

if __name__ == "__main__":
    app = QApplication()
    window = TestWindow()
    window.show()
    app.exec()

from PySide6.QtWidgets import (QApplication, QWidget, QPushButton)

import dawdreamer as daw
import numpy as np
from scipy.io import wavfile


class Vst():
    def __init__(self, sample_rate=44100, buffer_size=128):

        self.vst_path = "/Library/Audio/Plug-Ins/VST3/Serum.vst3"
        self.engine = daw.RenderEngine(sample_rate, buffer_size)
        self.plugin = self.engine.make_plugin_processor("Serum", self.vst_path)

    def vstEditer(self):
        print('open vst editer')
        self.plugin.open_editor()

    

'''
テスト用ウィンドウ
'''
class TestWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        vst = Vst()

        self.setWindowTitle('vstTest')
        self.resize(200, 110)

        load_vst_btn = QPushButton(self)
        load_vst_btn.move(20, 10)
        load_vst_btn.setText('load vst')
        # load_vst_btn.pressed.connect()

        vst_editer_btn = QPushButton(self)
        vst_editer_btn.move(20, 40)
        vst_editer_btn.setText('vst editer')
        vst_editer_btn.pressed.connect(lambda: vst.vstEditer())

        render_btn = QPushButton(self)
        render_btn.move(20, 70)
        render_btn.setText('render')
        # render_btn.pressed.connect()

if __name__ == "__main__":
    app = QApplication()
    window = TestWindow()
    window.show()
    app.exec()

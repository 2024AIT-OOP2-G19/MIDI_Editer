from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QFileDialog)

import dawdreamer as daw
import numpy as np
from scipy.io import wavfile
import os


class Vst():
    def __init__(self, sample_rate=44100, buffer_size=128):
        self.engine = daw.RenderEngine(sample_rate, buffer_size)
        self.vst_path = (str)
        self.plugin = (daw.PluginProcessor)
        self.isProcessorExists = False
        self.plugin_name = (str)

    def load_vst(self):
        file,check = QFileDialog.getOpenFileName(None, "ファイルを選択してください。","/Library/Audio/Plug-Ins","All Files (*);;vst Files (*.vst);;vst3 Files (*.vst3)")

        if check:
            self.vst_path = file
            self.plugin_name = os.path.splitext(os.path.basename(self.vst_path))[0] # パスからプラグイン名取得
            self.plugin = self.engine.make_plugin_processor(self.plugin_name, self.vst_path)

            assert self.plugin.get_name() == self.plugin_name # プラグインが反映されなかった時にエラー投げる

            self.isProcessorExists = True
            self.vst_editer()

    def vst_editer(self):
        if self.isProcessorExists == True:
            self.plugin.open_editor()
        else:
            self.load_vst()

    

'''
テスト用ウィンドウクラス
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
        load_vst_btn.pressed.connect(lambda: vst.load_vst())

        vst_editer_btn = QPushButton(self)
        vst_editer_btn.move(20, 40)
        vst_editer_btn.setText('vst editer')
        vst_editer_btn.pressed.connect(lambda: vst.vst_editer())

        render_btn = QPushButton(self)
        render_btn.move(20, 70)
        render_btn.setText('render')
        # render_btn.pressed.connect()

if __name__ == "__main__":
    app = QApplication()
    window = TestWindow()
    window.show()
    app.exec()

import PySide6
from PySide6.QtWidgets import (QApplication, QWidget, QPushButton)
from PySide6.QtGui import QIcon
from module.vst import Vst
import os
import sys
import module 

class MainWindow(QWidget):              # ウィンドウ系クラスを継承すること
    def __init__(self, parent=None):    # parentは他にウィンドウを表示させる場合に指定する
        super().__init__(parent)        # 継承元クラス（ここではQWidget）を初期化

        self.button1 = QPushButton("MIDI 保存", self)
        self.button1.setGeometry(50, 50, 100, 50)  

        self.button2 = QPushButton("音声書き出し", self)
        self.button2.setGeometry(150,50, 100, 50) 

        self.button3 = QPushButton("VST 読み込み", self)
        self.button3.setGeometry(50, 150, 100, 50) 

        self.button4 = QPushButton("VST 設定", self)
        self.button4.setGeometry(150, 150, 100, 50)

        self.button5 = QPushButton("", self)
        self.button5.setGeometry(130, 250, 30, 30)

        self.button6 = QPushButton("", self)
        self.button6.setGeometry(165, 250, 30, 30)

        self.button7 = QPushButton("", self)
        self.button7.setGeometry(95, 250, 30, 30) 

        icon_path = "再生.png"
        self.button5.setIcon(QIcon(icon_path))
        self.button5.setIconSize(self.button5.size())

        icon_path = "一時停止.png"
        self.button6.setIcon(QIcon(icon_path))
        self.button6.setIconSize(self.button6.size())

        icon_path = "最初.png"
        self.button7.setIcon(QIcon(icon_path))
        self.button7.setIconSize(self.button7.size())

        # ボタンのクリックイベントにスロットを接続
        self.button1.clicked.connect(self.on_button1_click)
        self.button2.clicked.connect(self.on_button2_click)
        self.button3.clicked.connect(self.on_button3_click)
        self.button4.clicked.connect(self.on_button4_click)
        self.button5.clicked.connect(self.on_button5_click)
        self.button6.clicked.connect(self.on_button6_click)
        self.button7.clicked.connect(self.on_button7_click)

    def on_button1_click(self):
        print("保存！")

    def on_button2_click(self):
        Vst.render_audio(midi_path, duration)

    def on_button3_click(self):
        Vst.load_vst()

    def on_button4_click(self):
        Vst.vst_editer()

    def on_button5_click(self):
        print("再生！！！")

    def on_button6_click(self):
        print("停止！！！")

    def on_button7_click(self):
        print("戻れ！！！")

if __name__ == "__main__":
    # 環境変数にPySide6を登録
    dirname = os.path.dirname(PySide6.__file__)
    plugin_path = os.path.join(dirname, 'plugins', 'platforms')
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
    
    app = QApplication(sys.argv)    # PySide6の実行
    window = MainWindow()           # ユーザがコーディングしたクラス
    window.show()                   # PySide6のウィンドウを表示
    sys.exit(app.exec())            # PySide6の終了

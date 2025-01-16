import PySide6
from PySide6.QtWidgets import QApplication, QWidget,  QPushButton, QFileDialog, QMessageBox, QLabel
import os
import sys
import subprocess
from main_layout import MainWindow



class TopWindow(QWidget):              # ウィンドウ系クラスを継承すること
    def __init__(self, parent=None): # parentは他にウィンドウを表示させる場合に指定する

        super().__init__(parent)        # 継承元クラス（ここではQWidget）を初期化
        self.setWindowTitle("作曲")
        self.resize(400,300)

        #タイトル
        self.label = QLabel("作曲ソフト",self)
        self.label.setGeometry(175,38,130,50)


        #1つ目のボタン
        self.button1 = QPushButton("最初から作る", self)
        self.button1.clicked.connect(self.on_button1_click)
        self.button1.setGeometry(140,160,130,50)


        #２つ目のボタン
        self.button2 = QPushButton("続きから作る", self)
        self.button2.clicked.connect(self.on_button2_click)
        self.button2.setGeometry(140,100,130,50)

    def on_button1_click(self):

        self.main_page = MainWindow()
        self.main_page.show()
        self.close()

    def on_button2_click(self,file_path):

        file_path,check = QFileDialog.getOpenFileName(None, "ファイルを選択してください。","","mid Files (*.mid)")

        if check:

            self.main_page = MainWindow(file_path) 

            self.main_page.show()
            self.close()

if __name__ == "__main__":
    # 環境変数にPySide6を登録
    dirname = os.path.dirname(PySide6.__file__)
    plugin_path = os.path.join(dirname, 'plugins', 'platforms')
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
    
    app = QApplication(sys.argv)    # PySide6の実行
    window = TopWindow()           # ユーザがコーディングしたクラス
    window.show()                   # PySide6のウィンドウを表示
    sys.exit(app.exec())            # PySide6の終了
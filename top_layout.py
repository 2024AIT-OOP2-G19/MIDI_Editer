import PySide6
from PySide6.QtWidgets import QApplication, QWidget,  QPushButton, QFileDialog, QMessageBox
import os
import sys
import subprocess
from main_layout import MainWindow

class TopWindow(QWidget):              # ウィンドウ系クラスを継承すること
    def __init__(self, parent=None):    # parentは他にウィンドウを表示させる場合に指定する
        super().__init__(parent)        # 継承元クラス（ここではQWidget）を初期化
        self.setWindowTitle("作曲")
        self.resize(400,300)

        #1つ目のボタン
        self.button1 = QPushButton("最初から作る", self)
        self.button1.clicked.connect(self.on_button1_click)
        self.button1.setGeometry(140,140,130,50)


        #２つ目のボタン
        self.button2 = QPushButton("続きから作る", self)
        self.button2.clicked.connect(self.on_button2_click)
        self.button2.setGeometry(140,80,130,50)

    def on_button1_click(self):
        print("最初から作るボタンがクリックされました")

    def on_button2_click(self):
        # subprocess.call(["open",'/Users'])
        #midiファイルの読み込み
        options = QFileDialog.Options()
        
        # ファイル選択ダイアログを開き、ユーザーが選択したファイルパスを取得
        file_path, _ = QFileDialog.getOpenFileName(
            self, "MIDIファイルを選択", "", "MIDI Files (*.mid);;All Files (*)", options=options
        )
        if file_path:
            # ユーザーがファイルを選択したときの通知
            QMessageBox.information(self, "MIDIファイル読み込み", f"選択されたファイル: {file_path}")
            print(f"MIDIファイルが読み込まれました: {file_path}") 
        else:
            # ファイル選択のキャンセル
            QMessageBox.warning(self, "キャンセル", "MIDIファイルの選択がキャンセルされました。")




if __name__ == "__main__":
    # 環境変数にPySide6を登録
    dirname = os.path.dirname(PySide6.__file__)
    plugin_path = os.path.join(dirname, 'plugins', 'platforms')
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
    
    app = QApplication(sys.argv)    # PySide6の実行
    window = TopWindow()           # ユーザがコーディングしたクラス
    window.show()                   # PySide6のウィンドウを表示
    sys.exit(app.exec())            # PySide6の終了
##ボタンを２つ作る
import PySide6
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel
from PySide6.QtGui import QPainter, QColor, QFont
from PySide6.QtCore import Qt, QRect
import os
import sys
from main_layout import MainWindow

class PianoBackground(QWidget):  # ピアノの鍵盤を縦に描画するウィジェット
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(300, 400)  # ウィンドウサイズ（縦長に変更）

    def paintEvent(self, event):  # paintEventでイベントを処理
        painter = QPainter(self)  # QPainterのインスタンスを作成
        painter.setRenderHint(QPainter.Antialiasing)  # アンチエイリアスを設定

        # 鍵盤の基本情報（縦向きに変更）
        key_width = 200  # 白鍵の幅
        key_height = 50  # 白鍵の高さ
        black_key_width = 70  # 黒鍵の幅
        black_key_height = 30  # 黒鍵の高さ
        num_keys = 7  # 白鍵の数

        # 白鍵を描画（縦向き）
        for i in range(num_keys):
            y = i * key_height
            rect = QRect(0, y, key_width, key_height)
            painter.setBrush(QColor("white"))
            painter.setPen(Qt.black)
            painter.drawRect(rect)

        # 黒鍵を描画（1, 2, 4, 5, 6番目の白鍵に黒鍵が付く）
        black_keys_positions = [0, 1, 2, 4, 5]
        for i in black_keys_positions:
            y =i * key_height + 35   # 白鍵の上に黒鍵を配置
            rect = QRect(0, y, black_key_width, black_key_height)
            painter.setBrush(QColor("black"))
            painter.setPen(Qt.black)
            painter.drawRect(rect)

class TopWindow(QWidget):              # ウィンドウ系クラスを継承すること
    def __init__(self, parent=None): # parentは他にウィンドウを表示させる場合に指定する

        super().__init__(parent)        # 継承元クラス（ここではQWidget）を初期化
        self.setWindowTitle("作曲")
        self.resize(400, 300)

        # 背景にピアノ鍵盤を設定
        self.piano_background = PianoBackground(self)

        # タイトル
        self.label1 = QLabel("MUSIC", self)
        self.label1.setGeometry(206, 38, 130, 50)
        self.label2 = QLabel("STUDIO", self)
        self.label2.setGeometry(224, 77, 130, 50)
        
        # フォント設定
        font = QFont("Impact", 44, QFont.Bold)  # フォント名、サイズ、太さを指定
        self.label1.setFont(font)
        self.label2.setFont(font)

        # 1つ目のボタン
        self.button1 = QPushButton("new", self)
        font = QFont("Impact", 18, QFont.Bold) 
        self.button1.setFont(font)
        self.button1.setStyleSheet("background-color: white; color: black;")
        self.button1.clicked.connect(self.on_button1_click)
        self.button1.setGeometry(75, 150, 125, 50)

        # 2つ目のボタン
        self.button2 = QPushButton("load", self)
        font = QFont("Impact", 18, QFont.Bold) 
        self.button2.setFont(font)
        self.button2.setStyleSheet("background-color: white; color: black;")
        self.button2.clicked.connect(self.on_button2_click)
        self.button2.setGeometry(75, 200, 125, 50)

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
    window = TopWindow()            # ユーザがコーディングしたクラス
    window.show()                   # PySide6のウィンドウを表示
    sys.exit(app.exec())            # PySide6の終了


from module.midi_edit import MidiEdit
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QGraphicsView, QGraphicsScene,
    QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QSplitter, QToolBar
)
from PySide6.QtGui import QBrush, QColor, QPen, QAction
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ピアノロール GUI")
        self.setGeometry(100, 100, 1500, 1000)

        '''
        ノートを追加するボタンとツールバーを作ったのですが、ダブルクリックでカーソル位置にノートを出せるようにするとのことです。
        念の為残しておきます。
        消してもらって構いません
        
        - やって欲しいこと
            - ダブルクリックした時にカーソル位置にノートを四分音符で配置すること
        '''
        # ツールバーを作成
        self.toolbar = QToolBar("ツールバー")
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        # ノート追加ボタンをツールバーに追加
        self.add_note_action = QAction("ノート追加", self)
        self.add_note_action.triggered.connect(self.add_note)
        self.toolbar.addAction(self.add_note_action)

        # メインウィジェットとスプリッター（左右分割）
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        splitter = QSplitter(Qt.Horizontal)

        # 左側のボタンスペース
        '''
        ここはテストで作ったので変更お願いします
        - やって欲しいこと
            - MIDI保存ボタンの作成
            - 音声書きしボタンの作成
            - VST読み込みボタンの作成
            - VST設定ボタンの作成
        '''
        button_widget = QWidget()
        button_layout = QVBoxLayout(button_widget)
        self.play_button = QPushButton("再生")
        self.stop_button = QPushButton("停止")
        self.record_button = QPushButton("録音")
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.record_button)
        button_layout.addStretch()  # ボタン下にスペースを追加

        # 右側のピアノロールスペース
        piano_widget = QWidget()
        piano_layout = QVBoxLayout(piano_widget)

        # 上部の小節スペース
        self.bar_scene = QGraphicsScene()
        self.bar_view = QGraphicsView(self.bar_scene)
        self.bar_view.setFixedHeight(40)  # 小節エリアの高さを固定
        self.bar_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.bar_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 中央部分の（鍵盤 + ピアノロール）
        center_layout = QHBoxLayout()
        self.keys_scene = QGraphicsScene()
        self.keys_view = QGraphicsView(self.keys_scene)
        self.keys_view.setFixedWidth(80)  # 鍵盤の幅を固定
        self.keys_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.roll_scene = QGraphicsScene()
        self.roll_view = QGraphicsView(self.roll_scene)
        self.roll_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.roll_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        center_layout.addWidget(self.keys_view)  # 鍵盤部分
        center_layout.addWidget(self.roll_view)  # ピアノロール部分

        # ピアノロールスペースに追加
        piano_layout.addWidget(self.bar_view)  # 小節エリア
        piano_layout.addLayout(center_layout)  # 鍵盤 + ピアノロール

        # スプリッターに左右を追加
        splitter.addWidget(button_widget) #　ボタンスペース
        splitter.addWidget(piano_widget) #ピアノロールスペース
        splitter.setStretchFactor(1, 3)  # ピアノロールのスペースを広くする

        # メインレイアウトにスプリッターを追加
        main_layout.addWidget(splitter)
        self.setCentralWidget(main_widget)

        # スクロールの同期
        self.roll_view.horizontalScrollBar().valueChanged.connect(
            self.bar_view.horizontalScrollBar().setValue
        )
        self.keys_view.verticalScrollBar().valueChanged.connect(
            self.roll_view.verticalScrollBar().setValue
        )
        self.roll_view.verticalScrollBar().valueChanged.connect(
            self.keys_view.verticalScrollBar().setValue
        )

        self.grid_size = 20  # グリッドのサイズ
        self.init_bar_area()
        self.init_piano_keys()
        self.init_piano_roll()

    def init_bar_area(self):
        """小節部分を初期化"""
        roll_width = 8090
        bar_width = self.grid_size * 16  # 1小節の幅（16グリット）
        bar_height = 40

        # 小節の描画
        for i in range(roll_width // bar_width):
            x = i * bar_width
            self.bar_scene.addRect(x+90, 0, bar_width, bar_height, QPen(Qt.black), QBrush(Qt.transparent))
            text_item = self.bar_scene.addText(str(i + 1))
            text_item.setPos(x + 95, 5)

        # シーンサイズを設定
        self.bar_scene.setSceneRect(0, 0, roll_width, bar_height)

    def init_piano_keys(self):
        """鍵盤部分を初期化"""
        key_height = self.grid_size
        keys = 60  # 鍵盤の数

        # 鍵盤の並び（C4から始まる）
        pattern = [True, False, True, False, True, True, False, True, False, True, False, True]
        pattern_length = len(pattern)

        for i in range(keys):
            y = (keys - i - 1) * key_height  # 鍵盤を下から並べる
            is_white = pattern[i % pattern_length]
            if is_white:
                color = QColor("white")
                self.keys_scene.addRect(0, y, 80, key_height, QPen(Qt.black), QBrush(color))
            else:
                color = QColor("black")
                self.keys_scene.addRect(
                    10, y + key_height * 0.25, 60, key_height * 0.5, QPen(Qt.black), QBrush(color)
                )

        # シーンサイズを設定
        self.keys_scene.setSceneRect(0, 0, 80, keys * key_height)

    def init_piano_roll(self):
        """ピアノロール部分を初期化"""
        roll_width = 8090
        key_height = self.grid_size
        keys = 60  # 鍵盤の数

        # グリッド線を描画
        for i in range(keys):
            y = (keys - i - 1) * key_height  # 鍵盤と同じ順序で下から描画
            for j in range(0, roll_width, self.grid_size):
                self.roll_scene.addRect(
                    j, y, self.grid_size, key_height, QPen(Qt.gray), QBrush(Qt.transparent)
                )

        # シーンサイズを設定
        self.roll_scene.setSceneRect(0, 0, roll_width, keys * key_height)


    '''
    ここも念の為残しておきます
    '''
    def add_note(self):
        """ノートを追加するボタンの処理"""
        note_width = self.grid_size * 4   # ノートの幅
        note_height = self.grid_size
        note = MidiEdit(100, 100, note_width, note_height, self.grid_size)
        self.roll_scene.addItem(note)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

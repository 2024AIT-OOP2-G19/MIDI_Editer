from module.note import Note
from module.note_manager import NoteManager
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QGraphicsView, QGraphicsScene,
    QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QSplitter, QToolBar
)
from PySide6.QtGui import QBrush, QColor, QPen, QAction
from PySide6.QtCore import Qt, QPoint

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ピアノロール GUI")
        self.setGeometry(100, 100, 1500, 1000)

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

        # 右側の部分をさらに分割
        right_splitter = QSplitter(Qt.Horizontal)

        # 右側を上下に分割した部分
        top_right_splitter = QSplitter(Qt.Vertical)

        # 右上にスペース部分（小節と同じ高さ）
        self.space_widget = QWidget()
        space_layout = QVBoxLayout(self.space_widget)
        space_layout.addStretch()  # スペース部分に空白を追加

        self.space_widget.setFixedHeight(40)  # 小節部分と同じ高さに設定

        # 右下に鍵盤部分
        self.keys_scene = QGraphicsScene()
        self.keys_view = QGraphicsView(self.keys_scene)
        self.keys_view.setFixedWidth(80)  # 鍵盤の幅を固定
        self.keys_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        top_right_splitter.addWidget(self.space_widget)  # スペース部分
        top_right_splitter.addWidget(self.keys_view)  # 鍵盤部分
        top_right_splitter.setStretchFactor(0, 1)
        top_right_splitter.setStretchFactor(1, 3)  # 鍵盤部分を広げる

        # 右側の右部分をさらに上下に分割
        bottom_right_splitter = QSplitter(Qt.Vertical)

        # 右上に小節部分
        self.bar_scene = QGraphicsScene()
        self.bar_view = QGraphicsView(self.bar_scene)
        self.bar_view.setFixedHeight(40)  # 小節エリアの高さを固定
        self.bar_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.bar_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 右下にピアノロール部分
        self.roll_scene = QGraphicsScene()
        self.roll_view = QGraphicsView(self.roll_scene)
        self.roll_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.roll_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        bottom_right_splitter.addWidget(self.bar_view)  # 小節部分
        bottom_right_splitter.addWidget(self.roll_view)  # ピアノロール部分
        bottom_right_splitter.setStretchFactor(1, 3)  # ピアノロール部分を広げる

        # 右側の右部分を配置
        right_splitter.addWidget(top_right_splitter)  # 鍵盤 + スペース
        right_splitter.addWidget(bottom_right_splitter)  # 小節 + ピアノロール
        right_splitter.setStretchFactor(0, 1)
        right_splitter.setStretchFactor(1, 3)  # ピアノロール部分を広げる

        # 左右を分割する
        splitter.addWidget(button_widget)  # ボタンスペース
        splitter.addWidget(right_splitter)  # 右側部分

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
        self.note_manager = NoteManager(self.grid_size)

    def init_bar_area(self):
        """小節部分を初期化"""
        roll_width = 8090
        bar_width = self.grid_size * 16  # 1小節の幅（16グリット）
        bar_height = 40

        # 小節の描画
        for i in range(roll_width // bar_width):
            x = i * bar_width
            self.bar_scene.addRect(x, 0, bar_width, bar_height, QPen(Qt.black), QBrush(Qt.transparent))
            text_item = self.bar_scene.addText(str(i + 1))
            text_item.setPos(x + 5, 5)

        # シーンサイズを設定
        self.bar_scene.setSceneRect(0, 0, roll_width, bar_height)

    def init_piano_keys(self):
        """鍵盤部分を初期化"""
        key_height = self.grid_size
        keys = 60  # 鍵盤の数

        # 鍵盤の並び（C4から始まる）
        pattern = [True, False, True, False, True, True, False, True, False, True, False, True]
        pattern_length = len(pattern)

        # ピアノのオクターブの最初のノートが何番目のCかを計算
        octave_start = 2  # C2から始める（中央C）


        for i in range(keys):
            print(i)
            y = i * key_height  # 鍵盤を下から並べる
            is_white = pattern[i % pattern_length]
            note_name = "C" if (i % pattern_length == 0) else None  # C の位置を判定
            if is_white:
                color = QColor("white")
                self.keys_scene.addRect(0, y, 80, key_height, QPen(Qt.black), QBrush(color))

                if note_name:
                    # ド（C）のラベルを追加
                    text_item = self.keys_scene.addText(f"{note_name}{octave_start}")
                    text_item.setDefaultTextColor(Qt.black)

                    # テキストを反転して正しく表示
                    text_item.setTransform(
                        text_item.transform().scale(1, -1), 
                        combine=True
                    )
                    text_item.setPos(45, y + key_height * 0.2 + self.grid_size-3)

                    # 次のCに進むときはオクターブをインクリメント
                    octave_start += 1
                
            else:
                color = QColor("black")
                self.keys_scene.addRect(
                    10, y + key_height * 0.25, 60, key_height * 0.5, QPen(Qt.black), QBrush(color)
                )

        # シーンサイズを設定
        self.keys_scene.setSceneRect(0, 0, 80, keys * key_height)

        # Y軸を反転して左下を (0, 0) に設定
        self.keys_view.setTransform(self.keys_view.transform().scale(1, -1))

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

        # Y軸を反転して左下を (0, 0) に設定
        self.roll_view.setTransform(self.roll_view.transform().scale(1, -1))
            


    def mouseDoubleClickEvent(self, event):
        """ダブルクリックイベントを処理してノートを配置"""
        if event.button() == Qt.LeftButton:
            if self.roll_view.underMouse():
                # シーン座標を取得
                position = self.roll_view.mapToScene(event.position().toPoint())
                offset_x = 198 # 鍵盤部分
                offset_y = -60 # 小節部分
                x = position.x() - offset_x
                y = position.y() - offset_y

                # グリッドにスナップ
                note_width = self.grid_size * 4  # 四分音符の幅
                note_height = self.grid_size
                note_x = round(x // self.grid_size) * self.grid_size 
                note_y = round(y // self.grid_size) * self.grid_size 

                # ノートをNoteManagerに追加
                note_id = self.note_manager.add_note(
                    left_x = note_x // self.grid_size,
                    right_x = (note_x + note_width) // self.grid_size,
                    y_pos = note_y // self.grid_size
                )
                print(f"Added Note ID: {note_id}, Position: {note_x}, {note_y}")
                # デバッグ情報を出力
                # print(f"Mouse Position: x={x}, y={y}")
                # print(f"Snapped Position: note_x={note_x}, note_y={note_y}")

                # ノートを作成してピアノロールに追加
                note = Note(note_x, note_y, note_width, note_height, self.grid_size)
                note.setData(0, note_id)  # NoteManagerのIDを設定
                self.roll_scene.addItem(note)
                print(f"Note Item Position: x={note.scenePos().x()}, y={note.scenePos().y()}")

    def remove_note_item(self, note_item):
        """指定されたノートアイテムを削除"""
        note_id = note_item.data(0)  # NoteManagerで管理されているノートIDを取得
        print(f"削除リクエスト: Note ID={note_id}")  # デバッグ
        if note_id:
            success = self.note_manager.remove_note(note_id)  # ノート情報を削除
            if success:
                self.roll_scene.removeItem(note_item)  # シーンからノートを削除
                print(f"削除成功: Note ID={note_id}")
            else:
                print(f"削除失敗: Note ID={note_id}")
    
    def update_note_info(self, note_item):
        """ノートの位置やサイズが変更された際に NoteManager を更新"""
        note_id = note_item.data(0)
        if note_id is not None:
            # ノートの現在の位置とサイズを取得
            rect = note_item.rect()
            pos = note_item.scenePos()
            grid_height_max = 59 # 0から59の60個

            left_x = round(pos.x() / self.grid_size)
            right_x = round((pos.x() + rect.width()) / self.grid_size)
            y_pos = grid_height_max + round(pos.y() / self.grid_size)

            # NoteManager を更新
            self.note_manager.update_note(note_id, left_x=left_x, right_x=right_x, y_pos=y_pos)

            # デバッグ情報
            print(f"Note Updated: ID={note_id}, left_x={left_x}, right_x={right_x}, y_pos={y_pos}")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

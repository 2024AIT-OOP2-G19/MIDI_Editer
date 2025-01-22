import PySide6
from PySide6.QtWidgets import (QApplication, QMainWindow, QGraphicsView, QGraphicsScene,
    QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QSplitter, QMessageBox, QSpinBox)
from PySide6.QtGui import QIcon, QBrush, QColor, QPen
from PySide6.QtCore import Qt
from module.note import Note
from module.note_manager import NoteManager
from module.midi_edit import note2midi, midi2note, y2pitch
from module.vst import Vst

from module.midi_rw import save_midi, load_midi

import os
import sys

class MainWindow(QMainWindow):
    def __init__(self, file_path=None):
        self.file_path = file_path
        self.midi = load_midi(file_path)
        print(self.file_path)
        
        super().__init__()
        self.setWindowTitle("Mono Track Studio ")
        self.setGeometry(100, 100, 1500, 1000)

        self.grid_size = 20  # グリッドのサイズ
        self.bpm = 120
        self.note_manager = NoteManager(self.grid_size)
        if file_path != None:
            self.note_manager.notes, self.bpm = midi2note(self.midi)

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
        
        button_style1 = """
    QPushButton {
        background-color: #2196f3;  /* 背景色 */
        color: #ffff00;               /* テキストの色 */
        border: 2px solid #388e3c;  /* ボーダーの色 */
        border-radius: 10px;        /* ボタンの角を丸くする */
        padding: 5px;               /* テキストの余白 */
    }
    QPushButton:hover {
        background-color: #1085dd;  /* ホバー時の背景色 */
    }
    QPushButton:pressed {
        background-color: #0060cc;  /* 押下時の背景色 */
    }
"""

        button_style2 = """
    QPushButton {
        background-color: #fbc02d;  /* 背景色 */
        color: #1033ff;               /* テキストの色 */
        border: 2px solid #ff9800;  /* ボーダーの色 */
        border-radius: 10px;        /* ボタンの角を丸くする */
        padding: 5px;               /* テキストの余白 */
    }
    QPushButton:hover {
        background-color: #dda01a;  /* ホバー時の背景色 */
    }
    QPushButton:pressed {
        background-color: #bb7000;  /* 押下時の背景色 */
    }
"""

        button_style3 = """
    QPushButton {
        background-color: #0097a7;  /* 背景色 */
        color: #222222;               /* テキストの色 */
        border: 2px solid #ff9800;  /* ボーダーの色 */
        border-radius: 10px;        /* ボタンの角を丸くする */
        padding: 5px;               /* テキストの余白 */
    }
    QPushButton:hover {
        background-color: #008c90;  /* ホバー時の背景色 */
    }
    QPushButton:pressed {
        background-color: #007787;  /* 押下時の背景色 */
    }
"""

        button_style4 = """
    QPushButton {
        background-color: #9e9e9e;  /* 背景色 */
        color: #222222;               /* テキストの色 */
        border: 2px solid #bbbbbb;  /* ボーダーの色 */
        border-radius: 10px;        /* ボタンの角を丸くする */
        padding: 5px;               /* テキストの余白 */
    }
    QPushButton:hover {
        background-color: #a2a2a2;  /* ホバー時の背景色 */
    }
    QPushButton:pressed {
        background-color: #b7b7b7;  /* 押下時の背景色 */
    }
"""

        play_button_img = os.path.join('images', '再生.png')
        play_pushing_img = os.path.join('images', '再生押してる.png')
        stop_button_img = os.path.join('images', '一時停止.png')
        stop_pushing_img = os.path.join('images', '一時停止押してる.png')
        self.button_widget = QWidget()
        button_layout = QVBoxLayout(self.button_widget)
        self.play_stop_widget = QWidget()
        play_stop_layout = QHBoxLayout(self.play_stop_widget)
        self.play_button = QPushButton("", self)
        self.set_button_images(self.play_button, play_button_img, play_pushing_img)
        self.stop_button = QPushButton("", self)
        self.set_button_images(self.stop_button, stop_button_img, stop_pushing_img)
        self.midi_save = QPushButton("MIDI 保存", self)
        self.midi_save.setStyleSheet(button_style1)
        self.sound_write = QPushButton("音声書き出し", self)
        self.sound_write.setStyleSheet(button_style2)
        self.vst_read = QPushButton("VST 読み込み", self)
        self.vst_read.setStyleSheet(button_style3)
        self.vst_option = QPushButton("VST 設定", self)
        self.vst_option.setStyleSheet(button_style4)

        button_layout.addWidget(self.play_stop_widget)
        play_stop_layout.addWidget(self.play_button)
        play_stop_layout.addWidget(self.stop_button)

        button_layout.addWidget(self.midi_save)
        button_layout.addWidget(self.sound_write)
        button_layout.addWidget(self.vst_read)
        button_layout.addWidget(self.vst_option)

        # テンポ設定用のスピンボックスを作成
        self.tempo_spinbox = QSpinBox()
        self.tempo_spinbox.setRange(10, 400)  # BPMの範囲を設定（10～400）
        self.tempo_spinbox.setValue(self.bpm)  # デフォルトのテンポを設定
        self.tempo_spinbox.setSuffix(" BPM")  # スピンボックスに単位を追加
        self.tempo_spinbox.valueChanged.connect(lambda: self.update_bpm(self.tempo_spinbox.value()))
        button_layout.addWidget(self.tempo_spinbox)

        
         # ボタンの外枠と焦点インジケータを完全に消す
        self.play_button.setStyleSheet("border: none; outline: none;")
        self.stop_button.setStyleSheet("border: none; outline: none;")

        # ボタンのクリックイベントにスロットを接続
        self.midi_save.clicked.connect(self.on_button1_click)
        self.sound_write.clicked.connect(self.on_button2_click)
        self.vst_read.clicked.connect(self.on_button3_click)
        self.vst_option.clicked.connect(self.on_button4_click)
        self.play_button.clicked.connect(self.on_button5_click)
        self.stop_button.clicked.connect(self.on_button6_click)

        button_layout.addStretch()  # ボタン下にスペースを追加



        # 右側の部分をさらに分割
        right_splitter = QSplitter(Qt.Horizontal)
        self.set_hundle_disabled(right_splitter)

        # 右側を上下に分割した部分
        top_right_splitter = QSplitter(Qt.Vertical)
        self.set_hundle_disabled(top_right_splitter)

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
        self.set_hundle_disabled(bottom_right_splitter)

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
        splitter.addWidget(self.button_widget)  # ボタンスペース
        splitter.addWidget(right_splitter)  # 右側部分

        splitter.widget(0).setFixedWidth(130) # ボタンスペースの幅設定
        self.set_hundle_disabled(splitter)

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

        self.init_bar_area()
        self.init_piano_keys()
        self.init_piano_roll()
        self.load_notes_from_manager()

        self.vst = Vst()

    def set_hundle_disabled(self, splitter:QSplitter):
        """
        splitterのハンドルを無効化
        """
        splitter.setStyleSheet(
            """
            QSplitter::handle {
            background: none;
            }
            """)
        splitter.setChildrenCollapsible(False)

    def set_button_images(self, button, normal_image, pressed_image):
        """
        ボタンに通常時と押下時の画像を設定
        """
        normal_icon = QIcon(normal_image)
        pressed_icon = QIcon(pressed_image)

        # 通常時のアイコンを設定
        button.setIcon(normal_icon)
        button.setIconSize(button.size())

        # 押下時と通常時のアイコンを切り替えるシグナル
        button.pressed.connect(lambda: button.setIcon(pressed_icon))
        button.released.connect(lambda: button.setIcon(normal_icon))

    def update_bpm(self, bpm:float):
        self.bpm = bpm
        print(f'bpm changed to {self.bpm}!')

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "確認", "MIDIファイルを保存しますか？",
                                     QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            self.midi = note2midi(self.note_manager.to_dict(), self.bpm)
            self.file_path = save_midi(self, self.midi, self.file_path) # midiファイルを保存
            event.accept()  # ウィンドウを閉じる
        elif reply == QMessageBox.No:
            event.accept()  # ウィンドウを閉じる
        else:
            event.ignore()  # ウィンドウを閉じない
            
    def init_bar_area(self):
        """小節部分を初期化"""
        roll_width = 64000
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
                    0, y, 80, key_height, QPen(Qt.black), QBrush(color)
                )

        # シーンサイズを設定
        self.keys_scene.setSceneRect(0, 0, 80, keys * key_height)

        # Y軸を反転して左下を (0, 0) に設定
        self.keys_view.setTransform(self.keys_view.transform().scale(1, -1))

    def init_piano_roll(self):
        """ピアノロール部分を初期化"""
        roll_width = 64000
        key_height = self.grid_size
        keys = 60  # 鍵盤の数

        # グリッド線を描画
        for i in range(keys):
            y = (keys - i - 1) * key_height  # 鍵盤と同じ順序で下から描画

            black = QColor(20, 20, 20) # 背景の色
            white = QColor(60, 60, 60)
            pattern = [white, black, white, black, white, white, black, white, black, white, black, white] # 背景パターン
            background_color = pattern[(i+5) % len(pattern)] # パターンに合わせて色設定
            self.roll_scene.addRect(0, y + key_height - self.grid_size, roll_width, key_height, QPen(Qt.black), QBrush(background_color)) # 背景設置

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
                offset_x = 238 # 鍵盤部分
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

                # 作成したノートの高さの音を鳴らす
                self.vst.play_note(y2pitch(note_y // self.grid_size))

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
            left_x = round((rect.x()+pos.x()) / self.grid_size)
            right_x = round(((rect.x()+pos.x()) + rect.width()) / self.grid_size)
            y_pos = round((rect.y()+pos.y()) / self.grid_size)

            # NoteManager を更新
            self.note_manager.update_note(note_id, left_x=left_x, right_x=right_x, y_pos=y_pos)

            self.vst.play_note(y2pitch(y_pos))

            # デバッグ情報
            print(f"Note Updated: ID={note_id}, left_x={left_x}, right_x={right_x}, y_pos={y_pos}")

    def load_notes_from_manager(self):
        """NoteManagerのデータを元にノートを再生成して表示"""
        data = self.note_manager.to_dict()
        print(data)  # 返り値を確認
        # 各ノートを再生成
        for note_id, note_data in data.items():
            print(type(note_data))  # note_data の型を確認
            # ノート情報を取得
            note_id = note_data["id"]
            left_x = note_data["left_x"] * self.grid_size
            right_x = note_data["right_x"] * self.grid_size
            y_pos = note_data["y_pos"] * self.grid_size

            # ノートの幅を計算
            note_width = right_x - left_x
            note_height = self.grid_size  # ノートの高さは1グリッド

            # ノートを生成
            note = Note(left_x, y_pos, note_width, note_height, self.grid_size)
            note.setData(0, note_id)  # NoteManagerのIDを設定

            # シーンに追加
            self.roll_scene.addItem(note)

            # デバッグ用出力
            print(f"Loaded Note ID: {note_id}, Position: x={left_x}, y={y_pos}, width={note_width}")

    def on_button1_click(self):
        print("保存！")
        self.midi = note2midi(self.note_manager.to_dict(), self.bpm)
        self.file_path = save_midi(self, self.midi, self.file_path) # midiファイルを保存

    def on_button2_click(self):
        self.file_path = save_midi(self, note2midi(self.note_manager.to_dict(), self.bpm), self.file_path)
        self.vst.render_audio(self.file_path, note2midi(self.note_manager.to_dict(), self.bpm).length + 4*(60/self.bpm))

    def on_button3_click(self):
        self.vst.load_vst()

    def on_button4_click(self):
        self.vst.vst_editer()

    def on_button5_click(self):
        self.file_path = save_midi(self, note2midi(self.note_manager.to_dict(), self.bpm), self.file_path)
        self.vst.play_midi_file(self.file_path, note2midi(self.note_manager.to_dict(), self.bpm).length + 4*(60/self.bpm))

    def on_button6_click(self):
        self.vst.stop_audio()
        print("停止！！！")

if __name__ == "__main__":
    # 環境変数にPySide6を登録
    dirname = os.path.dirname(PySide6.__file__)
    plugin_path = os.path.join(dirname, 'plugins', 'platforms')
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
    
    app = QApplication(sys.argv)    # PySide6の実行
    window = MainWindow()           # ユーザがコーディングしたクラス
    window.show()                   # PySide6のウィンドウを表示
    sys.exit(app.exec())            # PySide6の終了

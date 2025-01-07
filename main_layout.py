import PySide6
from PySide6.QtWidgets import (QApplication, QWidget, QMessageBox)
from module.midi_rw import save_midi
import os
import sys
import module 


class MainWindow(QWidget):              # ウィンドウ系クラスを継承すること
    def __init__(self, parent=None):    # parentは他にウィンドウを表示させる場合に指定する
        super().__init__(parent)        # 継承元クラス（ここではQWidget）を初期化
    
    def closeEvent(self, event):
        reply = QMessageBox.question(self, "確認", "MIDIファイルを保存しますか？",
                                     QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            save_midi(self.midi_file, self.file_path)
            event.accept()  # midiファイルを保存してウィンドウを閉じる
        elif reply == QMessageBox.No:
            event.accept()  # ウィンドウを閉じる
        else:
            event.ignore()  # ウィンドウを閉じない

if __name__ == "__main__":
    # 環境変数にPySide6を登録
    dirname = os.path.dirname(PySide6.__file__)
    plugin_path = os.path.join(dirname, 'plugins', 'platforms')
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
    
    app = QApplication(sys.argv)    # PySide6の実行
    window = MainWindow()           # ユーザがコーディングしたクラス
    window.show()                   # PySide6のウィンドウを表示
    sys.exit(app.exec())            # PySide6の終了

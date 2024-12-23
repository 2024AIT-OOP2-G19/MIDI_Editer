from PySide6.QtWidgets import QGraphicsRectItem
from PySide6.QtGui import QBrush, QColor, QCursor
from PySide6.QtCore import Qt

class MidiEdit(QGraphicsRectItem):
    def __init__(self, x, y, width, height, grid_size, *args, **kwargs):
        super().__init__(x, y, width, height, *args, **kwargs)
        self.setBrush(QBrush(QColor("blue"))) # ノートの色
        self.setFlags(QGraphicsRectItem.ItemIsMovable | QGraphicsRectItem.ItemIsSelectable) # setFlags(...)で移動・選択可能に設定
        self.setAcceptHoverEvents(True) # マウスカーソルがノート上にあるかを判定（eventという「オブジェクト」（QGraphicsSceneHoverEvent クラスのインスタンス）を引数に渡す）

        self.grid_size = grid_size
        self.resizing = False # リサイズ中かの判定、移動や選択とと混同しないように
        self.resize_margin = -90  # リサイズ判定範囲設定 （これが最適でした）

    def hoverMoveEvent(self, event): # eventでマウスカーソルの位置などを取得
        """マウスが右端に近づいたときにカーソルを変更"""
        if self.is_on_resize_area(event.pos()): #event.pos()でホバーイベントの発生した位置を取得
            self.setCursor(QCursor(Qt.SizeHorCursor))
        else:
            self.setCursor(QCursor(Qt.ArrowCursor))

    def mousePressEvent(self, event):
        '''右端でクリックされた場合、リサイズモードに入る'''
        if event.button() == Qt.LeftButton:
            if self.is_on_resize_area(event.pos()):
                self.resizing = True # リサイズ中
            else:
                super().mousePressEvent(event)

    '''
    mouseMoveEventで使うものの説明

    - event.pos()
        - eventでマウスカーソルの位置を取得
    - round()
        - 四捨五入
    - max()
        - グリッドサイズ以上になるようにする（１グリット以下にならないようにするため）
    
    snapped_width = max(self.grid_size, round(new_width / self.grid_size) * self.grid_size)の説明
    - round(new_width / self.grid_size) * self.grid_size
        - 現在のノートの幅をグリッドサイズで割って四捨五入し、どのグリットの倍数に近いかを判定。その後グリットサイズをかけてスナップ後の幅を求める。

    '''
    def mouseMoveEvent(self, event):
        if self.resizing: # リサイズ中かを判定
            '''リサイズ操作：ノート幅をグリッドにスナップ'''
            new_width = event.pos().x()
            if new_width > self.grid_size: # マウスカーソルのx座標が１グリットよりも大きかった場合ににリサイズを実行
                snapped_width = max(self.grid_size, round(new_width / self.grid_size) * self.grid_size) 
                self.setRect(self.rect().x(), self.rect().y(), snapped_width, self.rect().height())
        else:
            '''移動操作：ノートの位置をグリッドにスナップ'''
            # 移動操作：ノートの位置をグリッドにスナップ
            super().mouseMoveEvent(event)
            self.snap_to_grid()

    def mouseReleaseEvent(self, event):
        self.resizing = False # リサイズ中でない
        self.snap_to_grid()  # ドラッグ終了時にも位置をスナップ
        super().mouseReleaseEvent(event)

    def is_on_resize_area(self, pos):
        """リサイズ判定範囲を0.5グリッドに設定"""
        return self.rect().width() - pos.x() <= self.resize_margin

    def snap_to_grid(self):
        """グリッドに基づいて位置をスナップ"""
        x = round(self.scenePos().x() / self.grid_size) * self.grid_size
        y = round(self.scenePos().y() / self.grid_size) * self.grid_size
        self.setPos(x, y)
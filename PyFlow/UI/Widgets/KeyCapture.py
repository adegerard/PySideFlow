from PySide6.QtCore import (
    Qt,
    Signal,
)
from PySide6.QtGui import (
    QAction,
    QKeySequence,
)
from PySide6.QtWidgets import (
    QPushButton,
    QApplication,
)

class KeyCaptureWidget(QPushButton):
    """docstring for KeyCaptureWidget."""

    captured = Signal(object)

    def __init__(self, parent=None):
        super(KeyCaptureWidget, self).__init__(parent)
        self.bCapturing = False
        self._currentKey = None
        self.setText("NoKey")
        self.setCheckable(True)
        self.setToolTip(
            "<b>Left mouse button</b> to start capture.<br>Modifiers will not be accepted."
        )

        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.actionReset = QAction("Reset", None)
        self.actionReset.triggered.connect(self.resetToDefault)
        self.addAction(self.actionReset)

    def resetToDefault(self):
        self.setChecked(False)
        self.bCapturing = False
        self.currentKey = None

    @property
    def currentKey(self):
        return self._currentKey

    @currentKey.setter
    def currentKey(self, value):
        if value is None:
            self.setText("NoKey")
            self.bCapturing = False
            self.setChecked(False)
        else:
            self._currentKey = value
            self.setText(QKeySequence(self._currentKey).toString())
            self.bCapturing = False
            self.setChecked(False)
            self.captured.emit(self._currentKey)

    def mousePressEvent(self, event):
        super(KeyCaptureWidget, self).mousePressEvent(event)
        if event.button() == Qt.MouseButton.LeftButton and not self.bCapturing:
            if not self.bCapturing:
                self.bCapturing = True
                self.setText("capturing...")

    def keyPressEvent(self, event):
        super(KeyCaptureWidget, self).keyPressEvent(event)
        key = event.key()
        modifiers = event.modifiers()
        if modifiers == Qt.NoModifier:
            self.currentKey = Qt.Key(key)
        if not modifiers == Qt.NoModifier:
            self.resetToDefault()


if __name__ == "__main__":
    import sys

    a = QApplication(sys.argv)

    w = KeyCaptureWidget()
    w.show()

    sys.exit(a.exec_())

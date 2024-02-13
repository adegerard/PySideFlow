from PySide6.QtWidgets import *
from PySide6.QtGui import (
    QAction,
)
from PySide6.QtCore import (
    Qt,
    Signal,
)

class KeyboardModifiersCaptureWidget(QPushButton):
    """docstring for KeyboardModifiersCaptureWidget."""

    captured = Signal(object)

    def __init__(self, parent=None):
        super(KeyboardModifiersCaptureWidget, self).__init__(parent)
        self._currentModifiers = Qt.NoModifier
        self.setText("NoModifier")
        self.bCapturing = False
        self.setCheckable(True)
        self.setToolTip(
            "<b>Left click</b> to start capturing.<br><b>Enter</b> to accept.<br><b>Esc</b> to clear"
        )

        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.actionReset = QAction("Reset", None)
        self.actionReset.triggered.connect(self.resetToDefault)
        self.addAction(self.actionReset)

    def resetToDefault(self):
        self.currentModifiers = Qt.NoModifier
        self.bCapturing = False
        self.setChecked(False)

    @staticmethod
    def modifiersToString(modifiers):
        if modifiers == Qt.KeyboardModifier.NoModifier:
            return "NoModifier"
        return QtGui.QKeySequence(modifiers).toString()[:-2]

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if not self.bCapturing:
                self.bCapturing = True
                super(KeyboardModifiersCaptureWidget, self).mousePressEvent(event)
                self.setText("capturing...")

    @property
    def currentModifiers(self):
        return self._currentModifiers

    @currentModifiers.setter
    def currentModifiers(self, value):
        self._currentModifiers = value
        self.setText(self.modifiersToString(self._currentModifiers))
        self.captured.emit(self._currentModifiers)

    def keyPressEvent(self, event):
        super(KeyboardModifiersCaptureWidget, self).keyPressEvent(event)
        key = event.key()
        if key == Qt.Key_Escape:
            self.resetToDefault()
            self.bCapturing = False
            self.setChecked(False)
            return

        if key == Qt.Key_Return and self.bCapturing:
            self.bCapturing = False
            self.setChecked(False)
            self.update()

        if self.bCapturing:
            self.currentModifiers = event.modifiers()


if __name__ == "__main__":
    import sys

    a = QApplication(sys.argv)

    w = KeyboardModifiersCaptureWidget()
    w.show()

    sys.exit(a.exec_())

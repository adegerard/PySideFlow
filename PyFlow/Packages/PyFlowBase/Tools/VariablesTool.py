from PySide6.QtCore import (
    QSize,
)
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QVBoxLayout

from PyFlow.UI.Tool.Tool import DockTool
from PyFlow.UI.Views.VariablesWidget import VariablesWidget


class VariablesTool(DockTool):
    """docstring for Variables tool."""

    def __init__(self):
        super(VariablesTool, self).__init__()
        self.setMinimumSize(QSize(200, 50))
        self.varsWidget = None
        self.content = QWidget()
        self.content.setObjectName("VariablesToolContent")
        self.verticalLayout = QVBoxLayout(self.content)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.setWidget(self.content)

    @staticmethod
    def isSingleton():
        return True

    def onShow(self):
        super(VariablesTool, self).onShow()
        self.varsWidget = VariablesWidget(self.pyFlowInstance)
        self.pyFlowInstance.fileBeenLoaded.connect(self.varsWidget.actualize)
        self.verticalLayout.addWidget(self.varsWidget)
        self.varsWidget.actualize()

    def showEvent(self, event):
        super(VariablesTool, self).showEvent(event)
        if self.varsWidget is not None:
            self.varsWidget.actualize()

    @staticmethod
    def toolTip():
        return "Variables editing/creation"

    @staticmethod
    def name():
        return "Variables"

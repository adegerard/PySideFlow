from PySide6.QtCore import (
    QSize,
    Qt,
)

from PyFlow.UI.Tool.Tool import DockTool
from PyFlow.UI.Views.NodeBox import NodesBox


class NodeBoxTool(DockTool):
    """docstring for NodeBox tool."""

    def __init__(self):
        super(NodeBoxTool, self).__init__()
        self.content = None

    def onShow(self):
        super(NodeBoxTool, self).onShow()
        self.setMinimumSize(QSize(200, 50))
        self.content = NodesBox(
            self, self.pyFlowInstance.getCanvas(), False, False, bUseDragAndDrop=True
        )
        self.content.setObjectName("NodeBoxToolContent")
        self.setWidget(self.content)

    def refresh(self):
        self.content.treeWidget.refresh()

    @staticmethod
    def isSingleton():
        return True

    @staticmethod
    def defaultDockArea():
        return Qt.LeftDockWidgetArea

    @staticmethod
    def toolTip():
        return "Available nodes"

    @staticmethod
    def name():
        return "NodeBox"

from PyFlow.UI.Tool.Tool import ShelfTool
from PyFlow.Packages.PyFlowBase.Tools import RESOURCES_DIR
from PyFlow.Core.Common import Direction

from PySide6 import QtGui


class AlignBottomTool(ShelfTool):
    """docstring for AlignBottomTool."""

    def __init__(self):
        super(AlignBottomTool, self).__init__()

    @staticmethod
    def toolTip():
        return "Aligns selected nodes by bottom most node"

    @staticmethod
    def getIcon():
        return QtGui.QIcon(RESOURCES_DIR + "alignbottom.png")

    @staticmethod
    def name():
        return "AlignBottomTool"

    def do(self):
        self.pyFlowInstance.getCanvas().alignSelectedNodes(Direction.Down)

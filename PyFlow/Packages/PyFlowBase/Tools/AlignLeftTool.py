from PyFlow.UI.Tool.Tool import ShelfTool
from PyFlow.Packages.PyFlowBase.Tools import RESOURCES_DIR
from PyFlow.Core.Common import Direction

from PySide6 import QtGui


class AlignLeftTool(ShelfTool):
    """docstring for AlignLeftTool."""

    def __init__(self):
        super(AlignLeftTool, self).__init__()

    @staticmethod
    def toolTip():
        return "Aligns selected nodes by left most node"

    @staticmethod
    def getIcon():
        return QtGui.QIcon(RESOURCES_DIR + "alignleft.png")

    @staticmethod
    def name():
        return "AlignLeftTool"

    def do(self):
        self.pyFlowInstance.getCanvas().alignSelectedNodes(Direction.Left)

from PyFlow.UI.Tool.Tool import ShelfTool
from PyFlow.Packages.PyFlowBase.Tools import RESOURCES_DIR
from PyFlow.Core.Common import Direction

from PySide6 import QtGui


class AlignRightTool(ShelfTool):
    """docstring for AlignRightTool."""

    def __init__(self):
        super(AlignRightTool, self).__init__()

    @staticmethod
    def toolTip():
        return "Aligns selected nodes by right most node"

    @staticmethod
    def getIcon():
        return QtGui.QIcon(RESOURCES_DIR + "alignright.png")

    @staticmethod
    def name():
        return "AlignRightTool"

    def do(self):
        self.pyFlowInstance.getCanvas().alignSelectedNodes(Direction.Right)

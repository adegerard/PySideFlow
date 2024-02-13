from PyFlow.UI.Tool.Tool import ShelfTool
from PyFlow.Packages.PyFlowBase.Tools import RESOURCES_DIR
from PyFlow.Core.Common import Direction

from PySide6 import QtGui


class AlignTopTool(ShelfTool):
    """docstring for AlignTopTool."""

    def __init__(self):
        super(AlignTopTool, self).__init__()

    @staticmethod
    def toolTip():
        return "Aligns selected nodes by top most node"

    @staticmethod
    def getIcon():
        return QtGui.QIcon(RESOURCES_DIR + "aligntop.png")

    @staticmethod
    def name():
        return "AlignTopTool"

    def do(self):
        self.pyFlowInstance.getCanvas().alignSelectedNodes(Direction.Up)

from PyFlow.UI.Tool.Tool import FormTool
from PyFlow.Packages.PyFlowBase.Tools import RESOURCES_DIR
from PyFlow.UI.Forms.PackageBuilder import PackageBuilder as PB
from PySide6 import QtGui
from uuid import uuid4

class PackageBuilder(FormTool):
    """docstring for AlignBottomTool."""
    def __init__(self):
        super(PackageBuilder, self).__init__()
        self.guid = uuid4()

    @staticmethod
    def toolTip():
        return "Package Builder"

    def guid(self):
        return self.guid
    @staticmethod
    def getIcon():
        return QtGui.QIcon(RESOURCES_DIR + "options_icon.png")

    @staticmethod
    def getSmallIconPath():
        return RESOURCES_DIR + "new_file_icon.png"

    @staticmethod
    def getLargeIconPath():
        return RESOURCES_DIR + "new_file_icon.png"

    @staticmethod
    def name():
        return str("PackageBuilder")

    def do(self):
        self.pyFlowInstance.newFileFromUi(PB.PackageBuilder())

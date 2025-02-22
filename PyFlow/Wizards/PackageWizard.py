import os
import shutil

from PySide6 import QtCore
from PySide6.QtCore import (
    Qt,
)
from PySide6 import QtGui
from PySide6.QtWidgets import *

from PyFlow import Wizards
from PyFlow.Wizards.WizardDialogueBase import WizardDialogueBase
from PyFlow.Wizards.PkgGen import *
from PyFlow import Packages


class PackageWizard(WizardDialogueBase):
    """docstring for PackageWizard."""

    def __init__(self, parent=None):
        super(PackageWizard, self).__init__(parent)

    def addFinalPage(self):
        self.addPageWidget(
            QWidget(),
            "Everything is ready! Click done to generate the package!"
            + "\n\n**Note**: When job will be done, you will need to restart the editor in order to see your new stuff!"
            + "\nGood luck!",
        )

    def onDone(self):
        # if we are here, everything is correct
        packageName = self.lePkgName.text()
        includeUINodeFactory = (
            self.cbIncludeUINodeFactory.checkState() == Qt.Checked
            and self.cbIncludeUINodeFactory.isEnabled()
        )
        IncludeUIPinFactory = (
            self.cbUIPinFactory.checkState() == Qt.Checked
            and self.cbUIPinFactory.isEnabled()
        )
        IncludePinInputWidgetFactory = (
            self.cbPinInputWidgetFactory.checkState() == Qt.Checked
            and self.cbPinInputWidgetFactory.isEnabled()
        )
        IncludePrefsWidget = self.cbPrefsWidget.checkState() == Qt.Checked
        generatePackage(
            packageName,
            self.pbOutPathSelect.text(),
            bIncludeClassNode=self.cbIncludeClassNode.checkState() == Qt.Checked,
            bIncludeFooLib=self.cbIncludeFooLib.checkState() == Qt.Checked,
            bIncludeUINodeFactory=includeUINodeFactory,
            bIncludePin=self.cbIncludePin.checkState() == Qt.Checked,
            bIncludeUIPinFactory=IncludeUIPinFactory,
            bIncludeTool=self.cbIncludeTool.checkState() == Qt.Checked,
            bIncludeExporter=self.cbIncludeExporter.checkState() == Qt.Checked,
            bIncludePinInputWidgetFactory=IncludePinInputWidgetFactory,
            bIncludePrefsWindget=IncludePrefsWidget,
        )
        self.accept()

    def populate(self):
        # first page
        self.p1 = QWidget()
        self.p1Layout = QHBoxLayout(self.p1)
        self.lePkgName = QLineEdit("DemoPackage")
        # allow only letters without spaces
        self.lePkgName.setValidator(QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("^[A-Za-z]+$")))

        self.lePkgName.setAlignment(Qt.AlignCenter)
        self.p1Layout.addWidget(self.lePkgName)
        self.addPageWidget(self.p1, "Choose a name for your new package!")

        # second page
        self.p2 = QWidget()
        self.p2Layout = QVBoxLayout(self.p2)
        self.goToDocsWidget = QWidget()
        self.goToDocsLayout = QHBoxLayout(self.goToDocsWidget)
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.goToDocsLayout.addItem(spacer)
        self.bpGotoComponentsDocs = QPushButton("?")
        self.bpGotoComponentsDocs.setToolTip("Go to docs")
        self.bpGotoComponentsDocs.clicked.connect(self.onGotoComponentsDocs)
        self.goToDocsLayout.addWidget(self.bpGotoComponentsDocs)
        self.p2Layout.addWidget(self.goToDocsWidget)
        self.cbIncludeClassNode = QCheckBox("Class node")
        self.cbIncludeClassNode.stateChanged.connect(self.checkIncludeUINodeFactory)
        self.cbIncludeFooLib = QCheckBox("Function library")
        self.cbIncludePin = QCheckBox("Pin")
        self.cbIncludePin.stateChanged.connect(self.checkUIPinFactories)
        self.cbIncludeTool = QCheckBox("Tool")
        self.cbIncludeExporter = QCheckBox("Exporter")

        self.classNodeLayout = QHBoxLayout()
        self.classNodeLayout.setSpacing(1)
        self.classNodeLayout.setContentsMargins(0, 0, 0, 0)
        self.cbIncludeUINodeFactory = QCheckBox("Include ui node factory")
        self.cbIncludeUINodeFactory.setEnabled(False)
        self.classNodeLayout.addWidget(self.cbIncludeClassNode)
        self.classNodeLayout.addWidget(self.cbIncludeUINodeFactory)
        self.p2Layout.addLayout(self.classNodeLayout)
        self.p2Layout.addWidget(self.cbIncludeFooLib)

        self.pinLayout = QHBoxLayout()
        self.pinLayout.setSpacing(1)
        self.pinLayout.setContentsMargins(0, 0, 0, 0)
        self.cbUIPinFactory = QCheckBox("Include ui pin factory")
        self.cbUIPinFactory.setEnabled(False)
        self.pinLayout.addWidget(self.cbIncludePin)
        self.pinLayout.addWidget(self.cbUIPinFactory)
        self.p2Layout.addLayout(self.pinLayout)

        self.toolLayout = QHBoxLayout()
        self.toolLayout.setSpacing(1)
        self.toolLayout.setContentsMargins(0, 0, 0, 0)
        self.cbPinInputWidgetFactory = QCheckBox("Include pin input widget factory")
        self.cbPinInputWidgetFactory.setEnabled(False)
        self.toolLayout.addWidget(self.cbIncludeTool)
        self.toolLayout.addWidget(self.cbPinInputWidgetFactory)
        self.p2Layout.addLayout(self.toolLayout)

        self.cbPrefsWidget = QCheckBox("Prefs widget")

        self.p2Layout.addWidget(self.cbIncludeExporter)
        self.p2Layout.addWidget(self.cbPrefsWidget)

        self.addPageWidget(
            self.p2,
            "What components should be included?",
            "Please select at least one component to include to package!",
            self.isPackaeModuleSelected,
        )

        # third page
        self.p3 = QWidget()
        self.p3Layout = QHBoxLayout(self.p3)
        self.pbOutPathSelect = QPushButton("...")
        self.p3Layout.addWidget(self.pbOutPathSelect)
        self.pbOutPathSelect.clicked.connect(self.onSelectPackageDirectory)
        self.addPageWidget(
            self.p3,
            "Select output directory for your new package!"
            + "\n\n**Note**: Output directory should be writable.",
            pageEnterCallback=self.onSelectPackageRootEntered,
        )

    def checkUIPinFactories(self, state):
        checked = self.cbIncludePin.checkState() == Qt.Checked
        self.cbPinInputWidgetFactory.setEnabled(checked)
        self.cbUIPinFactory.setEnabled(checked)

    def checkIncludeUINodeFactory(self, state):
        # ui node factories can be created now only for class nodes
        self.cbIncludeUINodeFactory.setEnabled(
            self.cbIncludeClassNode.checkState() == Qt.Checked
        )

    def onGotoComponentsDocs(self):
        print("Open components docs page")

    def onSelectPackageRootEntered(self):
        self.pbOutPathSelect.setText(Packages.__path__[0])

    def isPackaeModuleSelected(self):
        return any(
            [
                self.cbIncludeClassNode.checkState() == Qt.Checked,
                self.cbIncludeFooLib.checkState() == Qt.Checked,
                self.cbIncludePin.checkState() == Qt.Checked,
                self.cbIncludeTool.checkState() == Qt.Checked,
                self.cbIncludeExporter.checkState() == Qt.Checked,
            ]
        )

    def onSelectPackageDirectory(self, *args):
        packageName = self.lePkgName.text()
        packageRoot = QFileDialog.getExistingDirectory(
            self,
            "Choose folder",
            "Choose folder",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,
        )
        newPackagePath = os.path.join(packageRoot, packageName)
        newPackagePath = os.path.normpath(newPackagePath)
        self.pbOutPathSelect.setText(packageRoot)

    @staticmethod
    def run():
        instance = PackageWizard()
        instance.exec_()

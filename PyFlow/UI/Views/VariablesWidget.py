import json
from PySide6.QtCore import (
    Qt,
)
from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import (
    QListWidget,
    QListWidgetItem,
    QWidget,
    QAbstractItemView
)

from PyFlow.UI.EditorHistory import EditorHistory
from PyFlow.UI.Canvas.UIVariable import UIVariable
from PyFlow.UI.Views.VariablesWidget_ui import Ui_Form
from PyFlow.UI import editor_history
from PyFlow.Core.Common import *
from PyFlow.Core import graph_manager

VARIABLE_TAG = "VAR"
VARIABLE_DATA_TAG = "VAR_DATA"


class VariablesListWidget(QListWidget):
    """docstring for VariablesListWidget."""

    def __init__(self, parent=None):
        super(VariablesListWidget, self).__init__(parent)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionRectVisible(True)

    def mousePressEvent(self, event):
        super(VariablesListWidget, self).mousePressEvent(event)
        w = self.itemWidget(self.currentItem())
        if w:
            drag = QtGui.QDrag(self)
            mime_data = QtCore.QMimeData()
            varJson = w.serialize()
            dataJson = {VARIABLE_TAG: True, VARIABLE_DATA_TAG: varJson}
            mime_data.setText(json.dumps(dataJson))
            drag.setMimeData(mime_data)
            drag.exec_()


class VariablesWidget(QWidget, Ui_Form):
    """docstring for VariablesWidget"""

    def __init__(self, pyFlowInstance, parent=None):
        super(VariablesWidget, self).__init__(parent)
        self.setupUi(self)
        self.pyFlowInstance = pyFlowInstance
        graph_manager.graphChanged.connect(self.onGraphChanged)
        self.pbNewVar.clicked.connect(self.createVariable)
        self.listWidget = VariablesListWidget()
        self.lytListWidget.addWidget(self.listWidget)
        self.pyFlowInstance.newFileExecuted.connect(self.actualize)

    def actualize(self):
        self.clear()
        # populate current graph
        graph = graph_manager.activeGraph()
        if graph:
            for var in graph.getVarList():
                self.createVariableWrapperAndAddToList(var)

    def onGraphChanged(self, *args, **kwargs):
        self.actualize()

    def clear(self):
        """Does not remove any variable. UI only
        """
        self.listWidget.clear()

    def killVar(self, uiVariableWidget):
        variableGraph = uiVariableWidget._rawVariable.graph
        variableGraph.killVariable(uiVariableWidget._rawVariable)
        self.actualize()

        self.clearProperties()
        editor_history.saveState("Kill variable", modify=True)

    def createVariableWrapperAndAddToList(self, rawVariable):
        uiVariable = UIVariable(rawVariable, self)
        item = QListWidgetItem(self.listWidget)
        item.setSizeHint(QtCore.QSize(60, 20))
        self.listWidget.setItemWidget(item, uiVariable)
        return uiVariable

    def createVariable(
        self, dataType="BoolPin", accessLevel=AccessLevel.public, uid=None
    ):
        rawVariable = (
            graph_manager
            .activeGraph()
            .createVariable(dataType=dataType, accessLevel=accessLevel, uid=uid)
        )
        uiVariable = self.createVariableWrapperAndAddToList(rawVariable)
        editor_history.saveState("Create variable", modify=True)
        return uiVariable

    def clearProperties(self):
        self.pyFlowInstance.onRequestClearProperties()

    def onUpdatePropertyView(self, uiVariable):
        self.pyFlowInstance.onRequestFillProperties(uiVariable.createPropertiesWidget)

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:/GIT/PyFlow/PyFlow/UI/Widgets\GraphEditor_ui.ui',
# licensing of 'd:/GIT/PyFlow/PyFlow/UI/Widgets\GraphEditor_ui.ui' applies.
#
# Created: Tue Jun 11 12:28:18 2019
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(863, 543)
        MainWindow.setDocumentMode(True)
        MainWindow.setDockNestingEnabled(True)
        MainWindow.setDockOptions(
            QtWidgets.QMainWindow.AllowNestedDocks
            | QtWidgets.QMainWindow.AllowTabbedDocks
            | QtWidgets.QMainWindow.AnimatedDocks
        )
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setLocale(
            QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates)
        )
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setContentsMargins(1, 1, 1, 1)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.SceneWidget = QtWidgets.QWidget(self.centralwidget)
        self.SceneWidget.setObjectName("SceneWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.SceneWidget)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setContentsMargins(1, 1, 1, 1)
        self.gridLayout.setObjectName("gridLayout")
        self.widgetCurrentGraphPath = QtWidgets.QWidget(self.SceneWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.widgetCurrentGraphPath.sizePolicy().hasHeightForWidth()
        )
        self.widgetCurrentGraphPath.setSizePolicy(sizePolicy)
        self.widgetCurrentGraphPath.setObjectName("widgetCurrentGraphPath")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widgetCurrentGraphPath)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.layoutGraphPath = QtWidgets.QHBoxLayout()
        self.layoutGraphPath.setSpacing(2)
        self.layoutGraphPath.setContentsMargins(-1, 0, -1, 0)
        self.layoutGraphPath.setObjectName("layoutGraphPath")
        self.horizontalLayout_3.addLayout(self.layoutGraphPath)
        self.gridLayout.addWidget(self.widgetCurrentGraphPath, 1, 0, 1, 1)
        self.SceneLayout = QtWidgets.QGridLayout()
        self.SceneLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.SceneLayout.setObjectName("SceneLayout")
        self.gridLayout.addLayout(self.SceneLayout, 4, 0, 1, 1)
        self.CompoundPropertiesWidget = QtWidgets.QWidget(self.SceneWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.CompoundPropertiesWidget.sizePolicy().hasHeightForWidth()
        )
        self.CompoundPropertiesWidget.setSizePolicy(sizePolicy)
        self.CompoundPropertiesWidget.setObjectName("CompoundPropertiesWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.CompoundPropertiesWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.CompoundPropertiesWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.leCompoundName = QtWidgets.QLineEdit(self.CompoundPropertiesWidget)
        self.leCompoundName.setObjectName("leCompoundName")
        self.horizontalLayout_2.addWidget(self.leCompoundName)
        self.label = QtWidgets.QLabel(self.CompoundPropertiesWidget)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.leCompoundCategory = QtWidgets.QLineEdit(self.CompoundPropertiesWidget)
        self.leCompoundCategory.setObjectName("leCompoundCategory")
        self.horizontalLayout_2.addWidget(self.leCompoundCategory)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.CompoundPropertiesWidget, 2, 0, 1, 1)
        self.gridLayout_3.addWidget(self.SceneWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 863, 21))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)
        self.toolBar.addSeparator()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle( "PyFlow")
        self.label_2.setText( "Name:")
        self.label.setText( "Category:")
        self.toolBar.setWindowTitle( "toolBar")


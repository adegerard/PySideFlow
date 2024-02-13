from typing import Any
from PySide6.QtCore import (
    Signal,
    QObject,
)
from PyFlow.Core.Common import *
from PyFlow.Core.Common import SingletonDecorator
from PyFlow.Core import graph_manager
from PyFlow.ConfigManager import ConfigManager


class _EditorState:
    def __init__(self, text: str, modify):
        super().__init__()
        self.text = text
        self.editorState = graph_manager.serialize()
        self._modify = modify

    def modifiesData(self):
        return self._modify

    def __repr__(self):
        return self.text


class EditorHistory(QObject):

    statePushed = Signal(object)
    stateRemoved = Signal(object)
    stateSelected = Signal(object)

    def __init__(self):
        super().__init__()
        self.app = None
        self.stack = list()
        try:
            self._capacity = int(
                ConfigManager().getPrefsValue("PREFS", "General/HistoryDepth")
            )
        except:
            self._capacity = 10

        self.activeState = None

    def set_parent(self, app: Any) -> None:
        self.app = app

    # def shutdown(self):
    #     clearSignal(self.statePushed)
    #     clearSignal(self.stateRemoved)
    #     clearSignal(self.stateSelected)
    #     clearList(self.stack)

    def getStack(self):
        return self.stack

    def count(self):
        return len(self.stack)

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        self._capacity = value
        if value < len(self.stack):
            for i in range(len(self.stack) - value):
                state = self.stack.pop()
                self.stateRemoved.emit(state)

    def clear(self):
        clearList(self.stack)

    def stateIndex(self, state):
        if state in self.stack:
            return self.stack.index(state)
        return -1

    @property
    def currentIndex(self):
        if self.activeState is not None:
            return self.stateIndex(self.activeState)
        return -1

    def push(self, edState):

        if self.currentIndex < self.count() - 1:
            while True:
                index = self.count() - 1
                nextState = self.stack[index]
                if nextState == self.activeState:
                    break
                state = self.stack.pop()
                self.stateRemoved.emit(state)

        self.stack.append(edState)

        if len(self.stack) >= self.capacity:
            poppedState = self.stack.pop(0)
            self.stateRemoved.emit(poppedState)

        self.statePushed.emit(edState)
        self.activeState = edState
        self.stateSelected.emit(edState)

    def selectState(self, state):
        for st in self.stack:
            if state == st:
                self.app.loadFromData(st.editorState)
                self.activeState = st
                self.stateSelected.emit(st)
                break

    def select(self, index):
        index = clamp(index, 0, self.count() - 1)

        if index == self.currentIndex:
            return

        if len(self.stack) == 0:
            return

        stateData = self.stack[index].editorState

        self.app.loadFromData(stateData)

        state = self.stack[index]
        self.activeState = state
        self.stateSelected.emit(state)

    def saveState(self, text, modify=False):
        self.push(_EditorState(text, modify))

    def undo(self):
        if self.currentIndex > 0:
            self.select(self.currentIndex - 1)

    def redo(self):
        self.select(self.currentIndex + 1)

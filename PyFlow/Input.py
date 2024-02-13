from collections import defaultdict
from enum import Enum

from PySide6 import QtCore, QtGui
from PySide6.QtCore import (
    Qt,
)
from PyFlow.Core.Common import *


class InputActionType(Enum):
    Mouse = 1
    Keyboard = 2


class InputAction(object):
    def __init__(
            self,
            name="defaultName",
            actionType=InputActionType.Keyboard,
            group="default",
            mouse=Qt.NoButton,
            key=None,
            modifiers=Qt.NoModifier,
    ):
        self.__actionType = actionType
        self._name = name
        self._group = group
        self.__data = {"mouse": mouse, "key": key, "modifiers": modifiers}

    def __str__(self):
        return "{0} {1} {2}".format(
            QtGui.QKeySequence(self.getModifiers()).toString(),
            self.getMouseButton().name.decode("utf=8"),
            QtGui.QKeySequence(self.getKey()).toString(),
        )

    @property
    def group(self):
        return self._group

    @property
    def actionType(self):
        return self.__actionType

    def __eq__(self, other):
        sm = self.__data["mouse"]
        sk = self.__data["key"]
        smod = self.__data["modifiers"]
        om = other.getData()["mouse"]
        ok = other.getData()["key"]
        omod = other.getData()["modifiers"]
        return all([sm == om, sk == ok, smod == omod])

    def __ne__(self, other):
        sm = self.__data["mouse"]
        sk = self.__data["key"]
        smod = self.__data["modifiers"]
        om = other.getData()["mouse"]
        ok = other.getData()["key"]
        omod = other.getData()["modifiers"]
        return not all([sm == om, sk == ok, smod == omod])

    def getName(self):
        return self._name

    def getData(self):
        return self.__data

    def setMouseButton(self, btn):
        assert isinstance(btn, Qt.MouseButton)
        self.__data["mouse"] = btn

    def getMouseButton(self):
        return self.__data["mouse"]

    def setKey(self, key=None):
        if key is None:
            key = []
        assert isinstance(key, Qt.Key)
        self.__data["key"] = key

    def getKey(self):
        return self.__data["key"]

    def setModifiers(self, modifiers=Qt.NoModifier):
        self.__data["modifiers"] = modifiers

    def getModifiers(self):
        return self.__data["modifiers"]

    @staticmethod
    def _modifiersToList(mods):
        result = []
        if mods & Qt.ShiftModifier:
            result.append(Qt.ShiftModifier)
        if mods & Qt.ControlModifier:
            result.append(Qt.ControlModifier)
        if mods & Qt.AltModifier:
            result.append(Qt.AltModifier)
        if mods & Qt.MetaModifier:
            result.append(Qt.MetaModifier)
        if mods & Qt.KeypadModifier:
            result.append(Qt.KeypadModifier)
        if mods & Qt.GroupSwitchModifier:
            result.append(Qt.GroupSwitchModifier)
        return result

    @staticmethod
    def _listOfModifiersToEnum(modifiersList):
        result = Qt.NoModifier
        for mod in modifiersList:
            result = result | mod
        return result

    def toJson(self):
        saveData = {"name": self._name,
                    "group": self._group,
                    "mouse": int(self.__data["mouse"].value),
                    "actionType": self.actionType.value}
        key = self.__data["key"]
        saveData["key"] = int(key) if key is not None else None

        modifiersList = self._modifiersToList(self.__data["modifiers"])

        saveData["modifiers"] = [i.value for i in modifiersList]
        return saveData

    def fromJson(self, jsonData):
        try:
            self._name = jsonData["name"]
            self._group = jsonData["group"]
            self.__data["mouse"] = Qt.MouseButton(jsonData["mouse"])
            keyJson = jsonData["key"]
            self.__data["key"] = (
                Qt.Key(keyJson) if isinstance(keyJson, int) else None
            )
            self.__data["modifiers"] = self._listOfModifiersToEnum(
                [Qt.KeyboardModifier(i) for i in jsonData["modifiers"]]
            )
            self.__actionType = InputActionType(jsonData["actionType"])
            return self
        except:
            return None


@SingletonDecorator
class InputManager(object):
    """Holds all registered input actions."""

    def __init__(self, *args, **kwargs):
        self.__actions = defaultdict(list)

    def __getitem__(self, key):
        # try find input action by name
        if key in self.__actions:
            return self.__actions[key]
        return []

    def __contains__(self, item):
        return item.getName() in self.__actions

    def getData(self):
        return self.__actions

    def registerAction(self, action):
        if action not in self.__actions[action.getName()]:
            self.__actions[action.getName()].append(action)

    def loadFromData(self, data):
        for actionName, actionVariants in data.items():
            for variant in actionVariants:
                actionInstance = InputAction().fromJson(variant)
                self.registerAction(actionInstance)

    def serialize(self):
        result = defaultdict(list)
        for actionName in self.__actions:
            for actionVariant in self.__actions[actionName]:
                result[actionName].append(actionVariant.toJson())
        return result

from PySide6.QtCore import (
    QObject,
    Qt,
    Signal,
)
import json
import uuid

from PyFlow import getPinDefaultValueByType
from PyFlow.Core import GraphBase
from PyFlow.Core.Common import *
from PyFlow.Core.Interfaces import IItemBase


class Variable(IItemBase, QObject):
    """Variable representation

    :var nameChanged: Fired when variable name was changed
    :vartype nameChanged: :class:`~PySide6.QtCore.base.Signal`
    :var valueChanged: Fired when variable value was changed
    :vartype valueChanged: :class:`~PySide6.QtCore.base.Signal`
    :var dataTypeChanged: Fired when variable data type was changed
    :vartype dataTypeChanged: :class:`~PySide6.QtCore.base.Signal`
    :var structureChanged: Fired when variable structure was changed
    :vartype structureChanged: :class:`~PySide6.QtCore.base.Signal`
    :var accessLevelChanged: Fired when variable access level was changed
    :vartype accessLevelChanged: :class:`~PySide6.QtCore.base.Signal`
    :var killed: Fired when variable was killed
    :vartype killed: :class:`~PySide6.QtCore.base.Signal`
    :var graph: Reference to owning graph
    :vartype graph: :class:`~PyFlow.Core.GraphBase.GraphBase`
    """
    nameChanged = Signal(str)
    valueChanged = Signal(str)
    dataTypeChanged = Signal(str)
    structureChanged = Signal(str)
    accessLevelChanged = Signal(str)
    killed = Signal()

    def __init__(
        self,
        graph: GraphBase,
        value,
        name,
        dataType,
        accessLevel=AccessLevel.public,
        structure=StructureType.Single,
        uid=None,
    ):
        """Constructor

        :param graph: Owning graph
        :type graph: :class:`~PyFlow.Core.GraphBase.GraphBase`
        :param value: Variable value
        :type value: object
        :param name: Variable name
        :type name: str
        :param dataType: Variable data type
        :type dataType: str
        :param accessLevel: Variable access level
        :type accessLevel: :class:`~PyFlow.Core.Common.AccessLevel`
        :param structure: Variable structure
        :type structure: :attr:`~PyFlow.Core.Common.StructureType.Single`
        :param uid: Variable unique identifier
        :type uid: :class:`~uuid.UUID`
        """
        super(Variable, self).__init__()


        self.graph: GraphBase = graph

        self._name = name
        self._value = value
        self._dataType = dataType
        self._structure = structure
        self._accessLevel = accessLevel
        self._packageName = None
        self._uid = uuid.uuid4() if uid is None else uid
        assert isinstance(self._uid, uuid.UUID)
        self.updatePackageName()
        self._uiWrapper = None

    def getWrapper(self):
        if self._uiWrapper is not None:
            return self._uiWrapper()
        return None

    def setWrapper(self, wrapper):
        if self._uiWrapper is None:
            self._uiWrapper = weakref.ref(wrapper)

    def location(self):
        """Returns location of variable

        .. seealso:: :meth:`~PyFlow.Core.GraphBase.GraphBase.location`
        """
        return self.graph.location()

    def findRefs(self):
        """Returns all getVar and setVar instances for variable
        """
        return self.graph.graph_manager.findVariableRefs(self)

    def updatePackageName(self):
        self._packageName = findPinClassByType(self._dataType)._packageName

    @property
    def packageName(self):
        """Variable type package name

        :rtype: str
        """
        return self._packageName

    @packageName.setter
    def packageName(self, value):
        assert isinstance(value, str)
        self._packageName = value
        self.packageNameChanged.emit(value)  # TODO: nonexistent, single use

    @property
    def accessLevel(self):
        """Variable access level

        :rtype: :class:`~PyFlow.Core.Common.AccessLevel`
        """
        return self._accessLevel

    @accessLevel.setter
    def accessLevel(self, value):
        assert isinstance(value, AccessLevel)
        self._accessLevel = value
        self.accessLevelChanged.emit(value)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        assert isinstance(value, str)
        self._name = value
        self.nameChanged.emit(value)

    @property
    def value(self):
        """Variable value

        :rtype: object
        """
        return self._value

    @value.setter
    def value(self, value):
        # type checking if variable is not of any type
        if not self.dataType == "AnyPin":
            supportedDataTypes = findPinClassByType(self.dataType).supportedDataTypes()
            if self.dataType not in supportedDataTypes:
                return

        try:
            if self._value != value or type(self._value) != type(value):
                self._value = value
                self.valueChanged.emit(value)
        except:
            self._value = value
            self.valueChanged.emit(value)

    @property
    def dataType(self):
        """Variable data type

        :rtype: str
        """
        return self._dataType

    @dataType.setter
    def dataType(self, value):
        assert isinstance(value, str)
        if value != self._dataType:
            self._dataType = value
            self.updatePackageName()
            self.value = getPinDefaultValueByType(value)
            self.dataTypeChanged.emit(value)

    @property
    def structure(self):
        """Variable structure

        :rtype: :class:`~PyFlow.Core.Common.StructureType`
        """
        return self._structure

    @structure.setter
    def structure(self, value):
        assert isinstance(value, StructureType)
        if value != self._structure:
            self._structure = value
            if self._structure == StructureType.Array:
                self.value = list()
            if self._structure == StructureType.Dict:
                self.value = PFDict("IntPin", "BoolPin")
            self.structureChanged.emit(self._structure)

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, value):
        assert isinstance(value, uuid.UUID)
        self.graph.getVars()[value] = self.graph.getVars().pop(self._uid)
        self._uid = value

    def serialize(self):
        pinClass = findPinClassByType(self.dataType)

        template = Variable.jsonTemplate()

        uidString = str(self.uid)

        template["name"] = self.name
        if self.dataType == "AnyPin":
            template["value"] = None
        else:
            template["value"] = json.dumps(self.value, cls=pinClass.jsonEncoderClass())
        if self.structure == StructureType.Dict:
            template["dictKeyType"] = self.value.keyType
            template["dictValueType"] = self.value.valueType
        else:
            template["dataType"] = self.dataType
        template["structure"] = self.structure.name
        template["accessLevel"] = self.accessLevel.name
        template["package"] = self._packageName
        template["uuid"] = uidString

        return template

    @staticmethod
    def deserialize(graph, jsonData, *args, **kwargs):
        name = jsonData["name"]

        dataType = "BoolPin"
        if jsonData["structure"] == StructureType.Dict.name:
            keyDataType = jsonData["dictKeyType"]
            valueDataType = jsonData["dictValueType"]

            value = PFDict(keyDataType, valueDataType)
        else:
            dataType = jsonData["dataType"]

            if dataType != "AnyPin":
                pinClass = findPinClassByType(dataType)
                value = json.loads(jsonData["value"], cls=pinClass.jsonDecoderClass())
            else:
                value = getPinDefaultValueByType("AnyPin")

        accessLevel = AccessLevel[jsonData["accessLevel"]]
        structure = StructureType[jsonData["structure"]]
        uid = uuid.UUID(jsonData["uuid"])
        return Variable(graph, value, name, dataType, accessLevel, structure, uid)

    @staticmethod
    def jsonTemplate():
        """Returns dictionary with minimum required fields for serialization

        :rtype: dict
        """
        template = {
            "name": None,
            "value": None,
            "dataType": None,
            "accessLevel": None,
            "package": None,
            "uuid": None,
        }
        return template

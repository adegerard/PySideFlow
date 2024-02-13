from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR
from PyFlow.Core import graph_manager

class cliexit(NodeBase):
    def __init__(self, name):
        super(cliexit, self).__init__(name)
        self.inp0 = self.createInputPin(
            DEFAULT_IN_EXEC_NAME, "ExecPin", None, self.compute
        )

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType("ExecPin")
        helper.addInputStruct(StructureType.Single)
        return helper

    @staticmethod
    def category():
        return "CLI"

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return "Stops cli program loop"

    def compute(self, *args, **kwargs):
        man = graph_manager
        man.terminationRequested = True

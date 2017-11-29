from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide.Node import Node


DESC = """flifs boolean
"""


class Not(Node, NodeBase):
    def __init__(self, name, graph):
        super(Not, self).__init__(name, graph, spacings=Spacings)
        self.in_bool = self.add_input_port('in', DataTypes.Bool)
        self.out_bool = self.add_output_port('out', DataTypes.Bool)
        portAffects(self.in_bool, self.out_bool)

    @staticmethod
    def get_category():
        return 'Common'

    @staticmethod
    def description():
        return DESC

    def compute(self):

        in_bool = self.in_bool.get_data()
        try:
            self.out_bool.set_data(not in_bool, False)
        except Exception as e:
            print(e)

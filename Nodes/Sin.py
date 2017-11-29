from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide.Node import Node
import math

DESC = '''in radians
'''


class Sin(Node, NodeBase):
    def __init__(self, name, graph):
        super(Sin, self).__init__(name, graph, spacings=Spacings)
        self.inp0 = self.add_input_port('in', DataTypes.Float)
        self.out0 = self.add_output_port('out', DataTypes.Float)
        portAffects(self.inp0, self.out0)

    @staticmethod
    def get_category():
        return 'Math'

    @staticmethod
    def get_keywords():
        return ["algebra", "math", "trigonometry"]

    @staticmethod
    def description():
        return DESC

    def compute(self):

        data = self.inp0.get_data()
        try:
            self.out0.set_data(math.sin(data), False)
        except Exception as e:
            print(e)

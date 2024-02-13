from PyFlow.Core import PinBase


class IntPin(PinBase):
    """doc string for IntPin"""

    def __init__(self, name, parent, direction, **kwargs):
        super(IntPin, self).__init__(name, parent, direction, **kwargs)
        self.setDefaultValue(0)

    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def pinDataTypeHint():
        return "IntPin", 0

    @staticmethod
    def color():
        return (0, 168, 107, 255)

    @staticmethod
    def supportedDataTypes():
        return ("IntPin", "FloatPin")

    @staticmethod
    def internalDataStructure():
        return int

    @staticmethod
    def processData(data):
        return IntPin.internalDataStructure()(data)

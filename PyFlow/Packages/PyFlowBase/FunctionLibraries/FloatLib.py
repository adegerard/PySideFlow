from math import pi

from PyFlow.Core import FunctionLibraryBase, IMPLEMENT_NODE
from PyFlow.Core.Common import *


class FloatLib(FunctionLibraryBase):
    """doc string for FloatLib"""

    def __init__(self, packageName):
        super(FloatLib, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("FloatPin", 0.0),
        meta={NodeMeta.CATEGORY: "Math|Float", NodeMeta.KEYWORDS: ["lerp"]},
    )
    # Linear interpolate
    def lerpf(
        a=("FloatPin", 0.0),
        b=("FloatPin", 0.0),
        alpha=(
            "FloatPin",
            0.0,
            {
                PinSpecifiers.VALUE_RANGE: (0.0, 1.0),
                PinSpecifiers.DRAGGER_STEPS: [0.1, 0.01, 0.001],
            },
        ),
    ):
        """
        Linear interpolate
        """
        return lerp(a, b, clamp(alpha, 0.0, 1.0))

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("BoolPin", False),
        meta={NodeMeta.CATEGORY: "Math|Float", NodeMeta.KEYWORDS: []},
    )
    def nearlyEqual(
        a=("FloatPin", 0.0), b=("FloatPin", 0.0), abs_tol=("FloatPin", 0.0)
    ):
        return abs(a - b) < abs_tol

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("FloatPin", 0.0),
        meta={NodeMeta.CATEGORY: "Math|Float", NodeMeta.KEYWORDS: []},
    )
    def multByPi(a=("FloatPin", 0.0)):
        """
        Multiplies the input value by pi.
        """
        return a * pi

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("FloatPin", 0.0),
        meta={NodeMeta.CATEGORY: "Math|Float", NodeMeta.KEYWORDS: []},
    )
    def normalizeToRange(
        Value=("FloatPin", 0.0), RangeMin=("FloatPin", 0.0), RangeMax=("FloatPin", 0.0)
    ):
        """
        Returns Value normalized to the given range. (e.g. 20 normalized to the range 10->50 would result in 0.25)
        """
        if RangeMin == RangeMax:
            return RangeMin

        if RangeMin > RangeMax:
            RangeMin, RangeMax = RangeMax, RangeMin
        return (Value - RangeMin) / (RangeMax - RangeMin)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("FloatPin", 0.0),
        meta={NodeMeta.CATEGORY: "Math|Float", NodeMeta.KEYWORDS: []},
    )
    def roundf(
        Value=("FloatPin", 0.0),
        Digits=("IntPin", 0, {PinSpecifiers.VALUE_RANGE: (0, 323)}),
    ):
        """
        Round a number to a given precision in decimal digits.
        """
        return round(Value, Digits)

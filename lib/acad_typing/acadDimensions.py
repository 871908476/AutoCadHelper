from __future__ import annotations
from .acadInterface import IAcadEntity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class AcadDimension(IAcadEntity):
    pass


class AcadDim3PointAngular(IAcadEntity):
    pass


class AcadDimAligned(IAcadEntity):
    pass


class AcadDimAngular(IAcadEntity):
    pass


class AcadDimArcLength(IAcadEntity):
    pass


class AcadDimDiametric(IAcadEntity):
    pass


class AcadDimOrdinate(IAcadEntity):
    pass


class AcadDimRadial(IAcadEntity):
    pass


class AcadDimRadialLarge(IAcadEntity):
    pass


class AcadDimRotated(IAcadEntity):
    pass
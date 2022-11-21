from __future__ import annotations
from .acadInterface import IAcadInterface
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class AcadDatabasePreferences(IAcadInterface):
    """An object that specifies the settings for the current AutoCAD drawing. """
    pass


class AcadPreferences(IAcadInterface):
    """This object specifies the current AutoCAD settings. """
    pass

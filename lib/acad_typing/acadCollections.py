from __future__ import annotations
from typing import TYPE_CHECKING

from .acadInterface import IAcadCollection

if TYPE_CHECKING:
    from .acadObjects import AcadSelectionSet, AcadLayout


class AcadDictionaries(IAcadCollection):
    """
    A container object for storing and retrieving objects
    """

    def Add(self, *args, **kwargs) -> object:
        pass

    def Item(self, index: str | int):
        pass


class AcadMaterials(IAcadCollection):
    pass


class AcadGroups(IAcadCollection):
    """The collection of all groups in the drawing."""
    pass


class AcadLayers(IAcadCollection):
    """The collection of all layers in the drawing. """
    pass


class AcadLayouts(IAcadCollection['AcadLayout']):
    """The Layouts collection for the document. """
    pass


class AcadHyperlinks(IAcadCollection):
    """The collection of all hyperlinks for a given object. """
    pass


class AcadSelectionSets(IAcadCollection['AcadSelectionSet']):
    pass
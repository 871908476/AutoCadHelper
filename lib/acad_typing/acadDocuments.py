from __future__ import annotations
from typing import TYPE_CHECKING

from .acadInterface import IAcadInterface, IAcadCollection
from win32com.client import VARIANT

if TYPE_CHECKING:
    from .acadApplication import *
    from .acadCollections import AcadSelectionSets, AcadGroups, AcadLayers, AcadLayouts, AcadMaterials, AcadDictionaries
    from .acadBlocks import AcadBlocks, AcadModelSpace, AcadPaperSpace
    from .acadEntities import *
    from .acadEnums import *
    from .acadMenu import *
    from .acadObjects import *


class AcadDatabase(IAcadInterface):
    """The contents of an XRef block. """

    def __init__(self, prototype) -> None:
        super().__init__(prototype)

    @property
    def Blocks(self) -> AcadBlocks:
        """Gets the Blocks collection for the drawing. """
        pass

    @property
    def Dictionaries(self) -> AcadDictionaries:
        """
        Gets the Dictionaries collection for the document.
        """
        pass

    @property
    def DimStyles(self) -> AcadDimStyle:
        """Gets the DimStyles collection for the document. """
        pass

    @property
    def ElevationModelSpace(self) -> float:
        """Specifies the elevation setting in model space. """
        pass

    @ElevationModelSpace.setter
    def ElevationModelSpace(self, val: float):
        pass

    @property
    def ElevationPaperSpace(self) -> float:
        """Specifies the elevation setting in paper space. """
        pass

    @ElevationPaperSpace.setter
    def ElevationPaperSpace(self, val: float):
        """Specifies the elevation setting in paper space. """
        pass

    @property
    def Groups(self) -> AcadGroups:
        """Gets the Groups collection for the document."""
        pass

    @property
    def Layers(self) -> AcadLayers:
        """Gets the Layers collection for the document. """
        pass

    @property
    def Layouts(self) -> AcadLayouts:
        """Gets the Layouts collection for the document. """
        pass

    @property
    def Limits(self) -> Sequence[float]:
        """
        Specifies the drawing limits. 

        Returns:
            An array of four values.
            The first pair of values define the X and Y coordinates of the lower-left limit, the second pair of values define the X and Y coordinates of the upper-right limit. 
        """
        pass

    @Limits.setter
    def Limits(self, arr: VARIANT):
        """
        Specifies the drawing limits. 

        Args:
            arr (VARIANT): VARIANT(5 | 8192, x1,y1,x2,y2)
        """
        pass

    @property
    def Linetypes(self) -> AcadLinetype:
        """Gets the Linetypes collection for the document. """
        pass

    @property
    def Material(self) -> AcadMaterial:
        """Specifies the name of the material. """
        pass

    @Material.setter
    def Material(self, val: str):
        """Specifies the name of the material. """
        pass

    @property
    def ModelSpace(self) -> AcadModelSpace:
        """Gets the ModelSpace collection for the document. """
        pass

    @property
    def PaperSpace(self) -> AcadPaperSpace:
        """Gets the PaperSpace collection for the document. """
        pass

    @property
    def PlotConfigurations(self) -> AcadPlotConfiguration:
        """Gets the PlotConfigurations collection for the document. """
        pass

    @property
    def Preferences(self) -> AcadPreferences:
        """Gets the Preferences object. """
        pass

    @property
    def RegisteredApplications(self) -> AcadDocument:
        """Gets the RegisteredApplications collection for the document. """
        pass

    @property
    def SectionManager(self) -> AcadSectionManager:
        """Returns the section manager object. """
        pass

    @property
    def SummaryInfo(self) -> AcadDocument:
        """Specifies the properties of a drawing. """
        pass

    @property
    def TextStyles(self) -> AcadDocument:
        """Gets the TextStyles collection for the document. """
        pass

    @property
    def UserCoordinateSystems(self) -> AcadDocument:
        """Gets the UCSs collection for the document. """
        pass

    @property
    def Viewports(self) -> AcadDocument:
        """Gets the Viewports collection for the document. """
        pass

    @property
    def Views(self) -> AcadDocument:
        """Gets the Views collection for the document. """
        pass

    def Regen(self, opt: acRegenType | int) -> None:
        """Regenerates the entire drawing and recomputes the screen coordinates and view resolution for all objects."""
        pass

    def CopyObjects(self,
                    objects: Sequence[object],
                    owner: object = None,
                    IDPairs=None) -> Sequence[object]:
        """
        Duplicates multiple objects (deep cloning). 

        Args:
            objects (Sequence[object]): The array of primary objects to be copied. 
                All the objects must have the same owner, and the owner must belong to the database or document that is calling this method. 
            owner: The new owner for the copied objects. 
                If no owner is specified, the objects will be created with the same owner as the objects in the Objects array. 
            IDPairs: Information on what happened during the copy and translation process.
        """
        pass

    def HandleToObject(self, handle: str) -> object:
        """
        Gets the object that corresponds to the given handle. 

        Args:
            handle: The handle of the object to return. 

        Returns:
            object: The object that corresponds to the given handle. 
        """
        pass

    def ObjectIdToObject(self, id: int) -> object:
        """
        Gets the object that corresponds to the given object ID. 

        Args:
            id (int): The object ID of the object to return. 

        Returns:
            object: The object that corresponds to the given object ID. 
        """
        pass


class AcadDocument(AcadDatabase):
    """An AutoCAD drawing. """

    @property
    def Active(self) -> AcadDocument:
        """Determines if the document is the active document for the session. """
        pass

    @property
    def ActiveDimStyle(self) -> AcadDimStyle:
        """Specifies the active dimension style. """
        pass

    @ActiveDimStyle.setter
    def ActiveDimStyle(self, val: 'AcadDimStyle'):
        """Specifies the active dimension style. """
        pass

    @property
    def ActiveLayer(self) -> AcadLayer:
        """Specifies the active layer."""
        pass

    @ActiveLayer.setter
    def ActiveLayer(self, val: 'AcadLayer'):
        pass

    @property
    def ActiveLayout(self) -> AcadLayout:
        '''Makes the specified drawing active.'''
        pass

    @ActiveLayout.setter
    def ActiveLayout(self, val: 'AcadLayout'):
        pass

    @property
    def ActiveLinetype(self) -> AcadLinetype:
        pass

    @ActiveLinetype.setter
    def ActiveLinetype(self, val: 'AcadLinetype'):
        pass

    @property
    def ActiveMaterial(self) -> AcadMaterial:
        pass

    @ActiveMaterial.setter
    def ActiveMaterial(self, val: 'AcadMaterial'):
        pass

    @property
    def ActivePViewport(self) -> AcadPViewport:
        pass

    @ActivePViewport.setter
    def ActivePViewport(self, val: 'AcadPViewport'):
        pass

    @property
    def ActiveSelectionSet(self) -> AcadSelectionSet:
        pass

    @ActiveSelectionSet.setter
    def ActiveSelectionSet(self, val: 'AcadSelectionSet'):
        pass

    @property
    def ActiveSpace(self):
        pass

    @ActiveSpace.setter
    def ActiveSpace(self, val):
        pass

    @property
    def ActiveTextStyle(self) -> AcadTextStyle:
        pass

    @ActiveTextStyle.setter
    def ActiveTextStyle(self, val: 'AcadTextStyle'):
        pass

    @property
    def ActiveUCS(self) -> AcadUCS:
        pass

    @ActiveUCS.setter
    def ActiveUCS(self, val: 'AcadUCS'):
        pass

    @property
    def ActiveViewport(self) -> AcadViewport:
        pass

    @ActiveViewport.setter
    def ActiveViewport(self, val: 'AcadViewport'):
        pass

    @property
    def Application(self) -> AcadApplication:
        pass

    @property
    def FullName(self):
        pass

    @property
    def Height(self) -> float:
        pass

    @Height.setter
    def Height(self, val: float):
        pass

    @property
    def HWND(self) -> float:
        pass

    @property
    def Materials(self) -> AcadMaterials:
        pass

    @property
    def MSpace(self) -> bool:
        """Allows editing of the model from floating paper space viewports. """
        pass

    @MSpace.setter
    def MSpace(self, val: bool):
        """Allows editing of the model from floating paper space viewports. """
        pass

    @property
    def Name(self) -> str:
        """Specifies the name of the object. """
        pass

    @Name.setter
    def Name(self, val: str):
        """Specifies the name of the object. """
        pass

    @property
    def ObjectSnapMode(self) -> bool:
        """Specifies the setting of the object snap mode. """
        pass

    @ObjectSnapMode.setter
    def ObjectSnapMode(self, val: bool):
        pass

    @property
    def Path(self) -> str:
        pass

    @property
    def PickfirstSelectionSet(self) -> AcadSelectionSet:
        """Gets the pickfirst selection set. """
        pass

    @property
    def Plot(self) -> AcadPlot:
        """Gets the Plot object for the document. """
        pass

    @property
    def ReadOnly(self) -> bool:
        pass

    @property
    def Saved(self) -> bool:
        """Specifies if the document has any unsaved changes."""
        pass

    @property
    def SelectionSets(self) -> AcadSelectionSets:
        """Gets the SelectionSets collection for the document. """
        pass

    @property
    def Width(self) -> float:
        pass

    @Width.setter
    def Width(self, val: float):
        pass

    @property
    def WindowState(self):
        pass

    @WindowState.setter
    def WindowState(self, val):
        pass

    @property
    def WindowTitle(self) -> str:
        pass

    @property
    def Utility(self) -> AcadUtility:
        """Gets the Utility object for the document."""
        pass

    def Activate(self):
        """Makes the specified drawing active. """
        pass

    def AuditInfo(self, fix: bool) -> None:
        """Evaluates the integrity of the drawing."""
        pass

    def Close(self, save: bool = False, file: str = None) -> None:
        pass

    def EndUndoMark(self) -> None:
        """Marks the end of a block of operations. """
        pass

    def Export(self, file: str, ext: str, selection_set: 'AcadSelectionSet') -> None:
        """
        Exports an AutoCAD drawing or a group of saved layer settings to a file.

        Args:
            file (str): The name for the newly exported file.
            ext (str): This string should contain three characters specifying the type of file to export the drawing into.
                    Case is not important. Use one of the following extensions: .wmf, .sat, .eps, .dxf, or .bmp.
            selection_set (AcadSelectionSet): For WMF, SAT, and BMP formats, the selection set specifies the objects to be exported.
                    For EPS and DXF formats, the selection set is ignored and the entire drawing is exported.
        """
        pass

    def Import(self, file: str, insert_point: VARIANT, scale: float) -> None:
        """
        Imports a drawing or a group of saved layer settings from a file.

        Args:
            file (str): The name of the file to be imported.
            insert_point (VARIANT): The 3D WCS coordinates location in the current drawing where the imported file is placed.
            scale (float): The scale used to place the imported file.
        """
        pass

    def LoadShapeFile(self, full_name: str) -> None:
        """
        Loads a shape file (SHX).

        Args:
            full_name (str): The full path and name of the shape file to load.
        """
        pass

    def New(self, template_file_name: str) -> AcadDocument:
        """
        Creates a new document in SDI mode.

        Args:
            template_file_name (str): The full path and file name of the template file.
        """
        pass

    def Open(self, name: str, pwd: str = None) -> AcadDocument:
        """
        Opens an existing drawing file (DWG) and makes it the active document.

        Args:
            name (str): The full path and file name, or a valid URL address, of the drawing file to open.
                    If the drawing is in the folder specified by the SupportPath property, then the path is not needed and the file name is sufficient.
            pwd: Password to open an encrypted drawing.

        Returns:
            The Document object that represents the opened drawing file.

        """
        pass

    def GetVariable(self, name: str):
        """Gets the current setting of an AutoCAD system variable."""
        pass

    def SetVariable(self, name, val):
        """Sets the value of an AutoCAD system variable. """
        pass

    def SendCommand(self, cmd: str):
        """Sends a command string from a VB or VBA application to the document for processing. """
        pass

    def PostCommand(self, cmd: str) -> None:
        """
        Posts a command string to the document for execution when the document enters an idle state.

        Args:
            cmd (str): The command string to post.
        """
        pass

    def PurgeAll(self) -> None:
        """Removes unused named references such as unused blocks or layers from the document."""
        pass

    def StartUndoMark(self) -> None:
        """Marks the beginning of a block of operations."""
        pass

    def WBlock(self, file_name: str, selection_set: 'AcadSelectionSet') -> None:
        """
        Writes out the given selection set as a new drawing file.

        Args:
            file_name (str): The file name to write the selection set to.
            selection_set (AcadSelectionSet): The name of the selection set.
        """
        pass

    def Save(self) -> None:
        """
        Saves a document or group of layer property settings; no longer supported for menu groups. 

        When you save a document to a secure URL, a dialog box prompts the user for the necessary password information.
        """
        pass

    def SaveAs(self, FileName: str, FileType: acSaveAsType | int, SecurityParams: VARIANT) -> None:
        """
        Saves the document to a specified file

        Args:
            FileName (str): The full path and file name, or valid URL address, for the file. The active document takes on the new name.
            FileType (acSaveAsType): _description_
            SecurityParams (_type_): Security settings used to specify a digital signature for the drawing.
        """
        pass


class AcadDocuments(IAcadCollection[AcadDocument]):
    """The collection of all AutoCAD drawings that are open in the current session. """

    def __init__(self, prototype) -> None:
        super().__init__(prototype)

    def Pack(self, val) -> AcadDocument:
        return AcadDocument(val)

    def Open(self, file: str, Readonly=False) -> AcadDocument:
        pass

    def Close(self, save=False, file: str = None) -> None:
        pass

    @property
    def Application(self):
        pass

from __future__ import annotations
from .acadInterface import IAcadEntity, IAcadObject
from typing import TYPE_CHECKING, Sequence, Tuple
from win32com.client import VARIANT

if TYPE_CHECKING:
    from .acadBlocks import AcadBlock
    from .acadEnums import acPlotPaperUnits, acPlotRotation, acPlotType, acPlotScale


class AcadView(IAcadObject):
    pass


class XRecord(IAcadObject):
    """
    XRecord objects are used to store and manage arbitrary data.
    """

    def __init__(self, prototype) -> None:
        super().__init__(prototype)

    def Delete(self):
        pass

    def GetExtensionDictionary(self) -> AcadDictionary:
        pass

    def GetXData(self, appName: str, xDataType: Sequence[int], xDataValue: Sequence[object]):
        pass

    def SetXData(self, xDataType: Sequence[int], xDataValue: Sequence[object]):
        pass


class AcadPlot(object):

    def __init__(self, prototype) -> None:
        self.__prototype = prototype

    @property
    def Prototype(self):
        return self.__prototype

    def PlotToFile(self, plotFile: str, plotConfig: str = None):
        pass


class AcadDimStyle(IAcadObject):
    pass


class AcadLayer(IAcadObject):
    pass


class AcadDictionary(IAcadObject):
    """The collection of all dictionaries in the drawing. """

    @property
    def Count(self) -> int:
        """
        Gets the number of items in the object.

        Returns:
            int: The number of items in the object.
        """
        pass

    @property
    def Name(self) -> str:
        pass

    @Name.setter
    def Name(self, name: str):
        pass

    def GetName(self) -> str:
        """
        Gets the name (keyword) of an object in a dictionary.

        Returns:
            str: The name (keyword) of the object.
        """
        pass

    def AddObject(self, keyword: str, className: str) -> object:
        """
        Adds an object to a named dictionary.

        Args:
            keyword: The keyword to be listed in the dictionary for this object.
            className: The rxClassName of the object to be created in the dictionary.

        Returns:
            The newly created object.

        """
        pass

    def AddXrecord(self, keyword: str) -> XRecord:
        """
        Creates an XRecord object in any dictionary.

        Args:
            keyword: The name of the XRecord within the dictionary.

        Returns:
            The newly created XRecord object.

        """
        pass

    def GetObject(self, keyword: str) -> object:
        """
        Gets the object in a dictionary, given the name (keyword) of the object.

        Args:
            keyword: The name (keyword) of the object in the dictionary.

        Returns:
            The object corresponding to the given name (keyword).

        """
        pass

    def Item(self, index: int | str) -> object:
        """
        Gets the member object at a given index in a collection, group, or selection set.

        Args:
            index: The index location in the collection for the member item to query.
                    The index must be either an integer or a string. If an integer, the index must be between 0 and N-1, where N is the number of objects in the collection or selection set.

        Returns:
            The object at the given index location in the collection or selection set.


        """
        pass

    def Remove(self, keyword: str) -> object:
        """
        Removes a named object from the dictionary.

        Args:
            keyword: The name (keyword) of the object to be removed from the dictionary.


        Returns:
            The object being removed from the dictionary.

        """
        pass

    def Rename(self, oldName: str, newName: str):
        """
        Renames an item in a dictionary or a set of saved layer settings.

        Args:
            oldName (str): The current name (keyword) of the object in the dictionary, or the name of a set of saved layer settings.
            newName (str): The new name (keyword) for the object in the dictionary, or the new name of the saved layer settings.
        """
        pass

    def Replace(self, keyword: str, obj: object):
        """
        Replaces an item in the dictionary by a given item.

        Args:
            keyword: The name (keyword) of the object to be replaced.
            obj: The new object.

        """
        pass


class IAcadDimStyle(IAcadObject):
    pass


class AcadViewport(IAcadObject):
    pass


class AcadState(IAcadObject):
    pass


class AcadSectionManager(IAcadObject):
    pass


class AcadPlotConfiguration(IAcadObject):

    def __init__(self, prototype) -> None:
        super().__init__(prototype)

    @property
    def CanonicalMediaName(self) -> str:
        """
        Specifies the paper size by name.
        
        Returns:
            eg: ISO_full_bleed_A3_(420.00_x_297.00_MM)
        """
        pass

    @CanonicalMediaName.setter
    def CanonicalMediaName(self, val: str):
        pass

    @property
    def CenterPlot(self) -> bool:
        """Specifies the centering of the plot on the media. """
        pass

    @CenterPlot.setter
    def CenterPlot(self, val: bool):
        pass

    @property
    def ConfigName(self) -> str:
        """Specifies the plotter configuration name. """
        pass

    @ConfigName.setter
    def ConfigName(self, val: str):
        pass

    @property
    def ModelType(self) -> bool:
        """
        Specifies whether a plot configuration applies to model space or to all layouts.

        Returns:
            bool: 
                True: The plot configuration applies only to the Model Space tab, or the layout is the model space layout. 
                False: The plot configuration applies to all layouts, or the layout is a paper space layout.
        """
        pass

    @ModelType.setter
    def ModelType(self, val: bool):
        """Specifies the name of the object. """
        pass

    @property
    def Name(self) -> str:
        """Specifies the name of the object."""
        pass

    @Name.setter
    def Name(self, val: str):
        pass

    @property
    def PaperUnits(self) -> acPlotPaperUnits | int:
        """
        Specifies the units for the display of layout or plot configuration properties. 
        
        This property determines the units for the display of the layout or plot configuration in the user interface. 
        This property does not determine the units for input or query of the ActiveX Automation properties. 
        All ActiveX Automation properties are represented in millimeters or radians, regardless of the units settings. 
        Changes to this property will not be visible until after a regeneration of the drawing. Use the Regen method to regenerate the drawing. 


        Returns:
            AcadAcPlotPaperUnits: _description_
        """
        pass

    @PaperUnits.setter
    def PaperUnits(self, val: acPlotPaperUnits | int):
        pass

    @property
    def PlotHidden(self) -> bool:
        """
        Specifies if objects are to be hidden during a plot. 

        Returns:
            bool: 
                True: Hide objects during the plot. 
                False: Do not hide objects during the plot.
        """
        pass

    @PlotHidden.setter
    def PlotHidden(self, val: bool):
        pass

    @property
    def PlotOrigin(self) -> VARIANT:
        """
        Specifies the origin of the layout or plot configuration in WCS coordinates. 

        Returns:
            VARIANT: Variant (two-element array of doubles) 
        """
        pass

    @PlotOrigin.setter
    def PlotOrigin(self, val: VARIANT):
        pass

    @property
    def PlotRotation(self) -> acPlotRotation | int:
        """Specifies the rotation angle for the layout or plot configuration. """
        pass

    @PlotRotation.setter
    def PlotRotation(self, val: acPlotRotation | int):
        pass

    @property
    def PlotType(self) -> acPlotType:
        """Specifies the type of layout or plot configuration. """
        pass

    @PlotType.setter
    def PlotType(self, val: acPlotType):
        pass

    @property
    def PlotViewportBorders(self) -> bool:
        """
        Specifies if the viewport borders are to be plotted. 

        Returns:
            True: Plot the viewport borders. 
            False: Do not plot the viewport borders. 
        """
        pass

    @PlotViewportBorders.setter
    def PlotViewportBorders(self, val: bool):
        pass

    @property
    def PlotViewportsFirst(self) -> bool:
        """
        Specifies if all geometry in paper space viewports is plotted first. 

        Returns:
            True: Geometry in paper space viewports is plotted first, and the geometry in paper space is plotted last. 
            False: Paper space geometry is plotted first, and the geometry in paper space viewports is plotted last. 
        """
        pass

    @PlotViewportsFirst.setter
    def PlotViewportsFirst(self, val: bool):
        pass

    @property
    def PlotWithLineweights(self) -> bool:
        """
        Specifies whether objects plot with the lineweights they are assigned in the plot file, 
        or with the lineweights in the drawing file. 

        A plot configuration is similar to a layout; as both contain identical plot information. 
        The difference is that a layout is associated with a Block object containing the geometry to plot. 
        A plot configuration is not associated with a particular Block object. 
        A plot configuration is simply a named collection of plot settings available for use with any geometry. 

        Returns:
            True: Plot using the lineweights in the plot style. 
            False: Plot using the lineweights in the drawing file. 
        """
        pass

    @property
    def PlotWithPlotStyles(self) -> bool:
        """
        Specifies whether or not to plot using the plot styles that are applied to objects and defined in the plot style table. 

        The PlotWithPlotStyles property is equivalent to the Plot with Plot Styles option in AutoCAD. 

        """
        pass

    @PlotWithPlotStyles.setter
    def PlotWithPlotStyles(self, val: bool):
        pass

    @property
    def ScaleLineweights(self) -> bool:
        """
        Specifies if the lineweight is scaled with the rest of the geometry when a layout is printed. 

        By default, lineweights are printed at absolute size (not scaled). 

        The property disabled for the model space layout. 

        """
        pass

    @ScaleLineweights.setter
    def ScaleLineweights(self, val: bool):
        pass

    @property
    def ShowPlotStyles(self) -> bool:
        """
        Specifies whether or not plot styles and plot style names are displayed in the drawing. 

        Returns:
            True: Plot styles and plot style names are displayed and plotted. 
            False: Plot styles and plot style names are not displayed.
        """
        pass

    @ShowPlotStyles.setter
    def ShowPlotStyles(self, val: bool):
        pass

    @property
    def StandardScale(self) -> acPlotScale:
        """Specifies the standard scale for the layout, viewport, or plot configuration. """
        pass

    @StandardScale.setter
    def StandardScale(self, val: acPlotScale):
        pass

    @property
    def StyleSheet(self) -> str:
        """Specifies the style sheet for the layout or plot configuration. """
        pass

    @StyleSheet.setter
    def StyleSheet(self, val: str):
        pass

    @property
    def UseStandardScale(self) -> bool:
        """Specifies if the plot is to use a standard or custom scale."""
        pass

    @UseStandardScale.setter
    def UseStandardScale(self, val: bool):
        pass

    @property
    def ViewToPlot(self) -> str:
        """Specifies the name of the view to plot. """
        pass

    @ViewToPlot.setter
    def ViewToPlot(self, val: str):
        pass

    def CopyFrom(self, SourceObject: object) -> None:
        """
        Copies the settings for a dimension style, layout, or plot configuration. 

        Args:
            SourceObject (object): The source object to be copied. 
        """
        pass

    def GetCanonicalMediaNames(self) -> VARIANT:
        """
        Gets all available canonical media names for the specified plot device. 

        Returns:
            VARIANT: Variant (array of strings)
            The array of available media names for the specified plot device. 
        """
        pass

    def GetCustomScale(self, Numerator: float, Denominator: float) -> None:
        """
        Gets the custom scale for a layout or plot configuration. 

        Args:
            Numerator (float): The numerator in the scale ratio. This value represents the number of inches or mm for the scale. 
            Denominator (float): The denominator in the scale ratio. This value represents the number of drawing units for the scale.
        """
        pass

    def GetLocaleMediaName(self, name: str) -> str:
        """
        Gets the localized version of the canonical media name. 

        Args:
            name (str): The canonical media name to find the localized version of. 

        Returns:
            str: The localized version of the specified canonical media name.
        """
        pass

    def GetPaperMargins(self, LowerLeft: VARIANT, UpperRight: VARIANT) -> None:
        """
        Gets the margins for the layout or plot configuration. 

        Args:
            LowerLeft (VARIANT): Variant (two-element array of doubles) The X and Y values for the lower-left margin.
            UpperRight (VARIANT): Variant (two-element array of doubles) The X and Y values for the upper-right margin. 
        """
        pass

    def GetPaperSize(self, Width: float, Height: float) -> None:
        """
        Gets the width and height of the configured paper. 

        Args:
            Width (float): The width of the paper.
            Height (float): The height of the paper.
        """
        pass

    def GetPlotDeviceNames(self) -> Sequence[str]:
        """Gets all available plot device names. """
        pass

    def GetPlotStyleTableNames(self) -> Sequence[str]:
        """Gets all available plot style table names. """
        pass

    def GetWindowToPlot(self, LowerLeft: VARIANT, UpperRight: VARIANT) -> None:
        """
        Gets the coordinates that define the portion of the layout to plot. 

        Args:
            LowerLeft (VARIANT): Variant (two-element array of doubles) 
                The X and Y values for the lower-left window. 
            UpperRight (VARIANT): Variant (two-element array of doubles) 
                The X and Y values for the upper-right window
        """
        pass

    def RefreshPlotDeviceInfo(self) -> None:
        """
        Updates the plot, canonical media, and plot style table information to reflect the current system state. 
            
        It is recommended that you refresh your plot device information before you use GetCanonicalMediaNames, 
        GetPlotDeviceNames, or GetPlotStyleTableNames methods for a given AutoCAD session.
         After that, you need only refresh the information if some part of the device setup changes during the course of the session.  
        """
        pass

    def SetCustomScale(self, Numerator: float, Denominator: float) -> None:
        """
        Sets the custom scale for a layout or plot configuration. 

        Args:
            Numerator (float): The numerator in the scale ratio. This value represents the number of inches or mm for the scale. 
            Denominator (float): The denominator in the scale ratio. This value represents the number of drawing units for the scale.
        """
        pass

    def SetWindowToPlot(self, LowerLeft: VARIANT, UpperRight: VARIANT) -> None:
        """
        Sets the coordinates that define the portion of the layout to plot. 

        Args:
            LowerLeft (VARIANT): Variant (two-element array of doubles) 
                The X and Y values for the lower-left window. 
            UpperRight (VARIANT): Variant (two-element array of doubles) 
                The X and Y values for the upper-right window
        """
        pass


class AcadLayout(AcadPlotConfiguration):

    def __init__(self, prototype) -> None:
        super().__init__(prototype)

    @property
    def Block(self) -> AcadBlock:
        """Specifies the block associated with the layout or multileader style."""
        pass

    @property
    def TabOrder(self) -> int:
        """Specifies the tab order of a layout. """
        pass

    @TabOrder.setter
    def TabOrder(self, val: int):
        pass


class AcadLinetype(IAcadObject):
    pass


class AcadMaterial:
    pass


class AcadSelectionSet:
    pass


class AcadTextStyle:
    pass


class AcadUCS:
    pass


class AcadUtility:

    def GetPoint(self, prompt: str) -> Tuple[float, float, float]:
        pass

    def Prompt(self, msg: str) -> None:
        """
        Displays a prompt on the command line.

        Args:
            msg (str): The prompt to display
        """
        pass

    def GetEntity(self, prompt: str = None) -> Tuple[IAcadEntity, Tuple[float, float, float]]:
        """
        Gets an object interactively

        This method requires the AutoCAD user to select an object by picking a point on the graphics screen. If an object is picked, it is returned in the first parameter and the second parameter will contain the point picked in WCS coordinates. If the pick point is not on an object the call will fail. 

        The pick point returned by GetEntity does not necessarily lie on the selected object. The returned point represents the location of the crosshairs at the time of selection. The relationship between this point and the object varies depending on the size of the pickbox and the current zoom scale. 

        This method can retrieve an object even if it is not visible on the screen or if it is on a frozen layer. 


        Args:
            prompt (str): The text to display that prompts the user for input.

        Returns:
            Tuple[IAcadEntity,Tuple[float,float,float]]: 
                IAcadEntity: The picked object. Can be one of any of the drawing objects.
                Tuple[float,float,float]: A 3D WCS coordinate specifying the point that was selected.

        """

        pass

    def GetCorner(self, point: VARIANT, prompt: str = None) -> Tuple[float, float, float]:
        """
        Gets a corner of a rectangle. 

        Args:
            point (VARIANT): The 3D WCS coordinates specifying the base point of the rectangle
            prompt (str): The text to display that prompts the user for input.

        Returns:
            Tuple[float,float,float]: The 3D WCS coordinates representing the corner of the rectangle. 

        """
        pass

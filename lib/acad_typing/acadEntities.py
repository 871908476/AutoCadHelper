from __future__ import annotations

from .acadInterface import IAcadEntity
from win32com.client import VARIANT
from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from typing import Sequence
    from .acadBlocks import AcadDynamicBlockReferenceProperty
    from .acadEnums import *
    from .acadObjects import AcadView


class AcadAttributeReference(IAcadEntity):

    @property
    def Alignment(self) -> int | acAlignment:
        """Specifies both the vertical and horizontal alignments for the attribute, attribute reference, or text. """
        pass

    @Alignment.setter
    def Alignment(self, val: int | acAlignment):
        pass

    @property
    def Backward(self) -> bool:
        """
        Specifies the direction of text. 

        Returns:
            True: The text is backward. 
            False: The text is forward. 
        """
        pass

    @Backward.setter
    def Backward(self, val: bool):
        pass

    @property
    def Constant(self) -> bool:
        """
        Specifies whether the attribute or attribute reference is constant or not. 

        A constant attribute is one that maintains the same value in every occurrence. 
        AutoCAD does not prompt for a value of constant attributes. 
        An attribute can exist as only one of four optional modes: constant, preset, invisible, or verify. 

        The AFLAGS system variable stores the current mode settings. You can query the current mode using the Mode property.

        Returns:
            True: The attribute is a constant attribute. 
            False: The attribute is not a constant attribute. 
        """
        pass

    @property
    def FieldLength(self) -> int:
        """Specifies the field length of the attribute."""
        pass

    @FieldLength.setter
    def FieldLength(self, val: int):
        pass

    @property
    def Height(self) -> float:
        """Changes the height of the object."""
        pass

    @Height.setter
    def Height(self, val: float):
        pass

    @property
    def InsertionPoint(self) -> VARIANT:
        pass

    @InsertionPoint.setter
    def InsertionPoint(self, val: VARIANT):
        pass

    @property
    def Invisible(self) -> bool:
        """Specifies whether the attribute or attribute reference is invisible."""
        pass

    @Invisible.setter
    def Invisible(self, val: bool):
        """Specifies whether the attribute or attribute reference may be moved relative to the geometry in the block."""
        pass

    @property
    def LockPosition(self) -> bool:
        pass

    @property
    def MTextAttribute(self) -> bool:
        """
        Determines if the attribute is multiline.

        Returns:
            True: The attribute is multiline. 
            False: The attribute is single-line. 
        """
        pass

    @MTextAttribute.setter
    def MTextAttribute(self, val: bool):
        pass

    @property
    def MTextAttributeContent(self) -> str:
        """Gets the multiline attribute content."""
        pass

    @MTextAttributeContent.setter
    def MTextAttributeContent(self, val: str):
        pass

    @property
    def MTextBoundaryWidth(self) -> float:
        """Determines the width of the text boundary for the multiline attribute."""
        pass

    @MTextBoundaryWidth.setter
    def MTextBoundaryWidth(self, val: float):
        pass

    @property
    def MTextDrawingDirection(self) -> acDrawingDirection:
        """Determines the drawing direction for the multiline attribute."""
        pass

    @MTextDrawingDirection.setter
    def MTextDrawingDirection(self, val: acDrawingDirection):
        pass

    @property
    def Normal(self) -> VARIANT:
        """Specifies the three-dimensional normal unit vector for the object."""
        pass

    @Normal.setter
    def Normal(self, val: VARIANT):
        pass

    @property
    def ObliqueAngle(self) -> float:
        """
        Specifies the oblique angle of the object.

        Returns:
            float: The angle in radians within the range of -85 to +85 degrees.
                A positive angle denotes a lean to the right; a negative value will have 2*PI added to it to convert it to its positive equivalent. 
        """
        pass

    @ObliqueAngle.setter
    def ObliqueAngle(self, val: float):
        pass

    @property
    def Rotation(self) -> float:
        """Specifies the rotation angle for the object. """
        pass

    @Rotation.setter
    def Rotation(self, val: float):
        pass

    @property
    def ScaleFactor(self) -> float:
        """Specifies the scale factor for the object. """
        pass

    @ScaleFactor.setter
    def ScaleFactor(self, val: float):
        pass

    @property
    def StyleName(self) -> str:
        """Specifies the name of the style used with the object."""
        pass

    @StyleName.setter
    def StyleName(self, val: str):
        pass

    @property
    def TagString(self) -> str:
        """
        Specifies the tag string of the object.

        This string identifies each occurrence of the attribute. 
        Enter any characters except spaces or exclamation points.
        AutoCAD changes lowercase letters to uppercase.

        Returns:
            str: The tag string of the object. 

        """
        pass

    @TagString.setter
    def TagString(self, val: str):
        pass

    @property
    def TextAlignmentPoint(self) -> VARIANT:
        """
        Specifies the alignment point for text and attributes.

        This property will be reset to 0, 0, 0 and will become read-only when the Alignment property is set to acAlignmentLeft. 
        To position text whose justification is left, fit, or aligned, use the InsertionPoint property. 

        Returns:
            VARIANT: Variant (three-element array of doubles)
        """
        pass

    @TextAlignmentPoint.setter
    def TextAlignmentPoint(self, val: VARIANT):
        pass

    @property
    def TextGenerationFlag(self) -> acTextGenerationFlag:
        """Specifies the attribute text generation flag."""
        pass

    @TextGenerationFlag.setter
    def TextGenerationFlag(self, val: acTextGenerationFlag):
        pass

    @property
    def TextString(self) -> str:
        """
        Specifies the text string for the entity.

        This is equivalent to the value of the attribute in AutoCAD. 

        Returns:
            str: The maximum length is 256 characters.
        """
        pass

    @TextString.setter
    def TextString(self, val: str):
        pass

    @property
    def Thickness(self) -> float:
        """Specifies the distance a 2D AutoCAD object is extruded above or below its elevation."""
        pass

    @Thickness.setter
    def Thickness(self, val: float):
        pass

    @property
    def UpsideDown(self) -> bool:
        """
        Specifies the direction of text.

        Returns:
            True: The text is upside down. 
            False: The text is not upside down.
        """
        pass

    @UpsideDown.setter
    def UpsideDown(self, val: bool):
        pass

    def UpdateMTextAttribute(self) -> None:
        """Updates attribute from the multiline text and multiline text from an attribute."""
        pass


class AcadPoint(IAcadEntity):
    """
    A point marker appearing as a dot, square, circle, X, tick, or plus sign (+); or as a combination of these.
    """
    pass


class AcadPViewport(IAcadEntity):
    """Rectangular objects created in paper space that display views. """

    @property
    def ArcSmoothness(self) -> int:
        """
        Specifies the smoothness of circles, arcs, and ellipses. 
        """
        pass

    @property
    def Center(self) -> VARIANT:
        """
        Specifies the center of an arc, circle, ellipse, view, or viewport.

        Returns: Variant (three-element array of doubles)

        """
        pass

    @Center.setter
    def Center(self, value: VARIANT):
        """
        Specifies the center of an arc, circle, ellipse, view, or viewport.

        Args:
            value: Variant (three-element array of doubles)

        Returns:

        """
        pass

    @property
    def Clipped(self) -> bool:
        """Determines if the viewport has been clipped. """
        pass

    @property
    def CustomScale(self) -> float:
        """Specifies the custom scale factor for the viewport. """
        pass

    @CustomScale.setter
    def CustomScale(self, value: float):
        pass

    @property
    def Direction(self) -> VARIANT:
        """Specifies the viewing direction for a 3D visualization of the drawing, or the direction vector of the table."""
        pass

    @Direction.setter
    def Direction(self, value: VARIANT):
        """
        Specifies the viewing direction for a 3D visualization of the drawing, or the direction vector of the table.

        Args:
            value: VARIANT ( a three-element array of doubles )

        Returns:

        """
        pass

    @property
    def DisplayLocked(self) -> bool:
        """Specifies whether the viewport is locked. """
        pass

    @DisplayLocked.setter
    def DisplayLocked(self, value: bool):
        pass

    @property
    def GridOn(self) -> bool:
        """Specifies the status of the viewport grid."""
        pass

    @GridOn.setter
    def GridOn(self, value: bool):
        pass

    @property
    def HasSheetView(self) -> bool:
        """Specifies whether the viewport is linked to a corresponding sheet view. """
        pass

    @property
    def LabelBlockId(self) -> int:
        """
        Returns and sets the label block ID associated with the viewport.

        Returns:  Long_PTR
            The label block ID associated with the viewport.

        """
        pass

    @LabelBlockId.setter
    def LabelBlockId(self, value: int):
        pass

    @property
    def LayerPropertyOverrides(self) -> bool:
        """Specifies whether the external reference or viewport has layer property overrides."""
        pass

    @property
    def LensLength(self) -> float:
        """Specifies the lens length used in perspective viewing. """
        pass

    @property
    def ModelView(self) -> AcadView:
        """Returns and sets the model view associated with the viewport. """
        pass

    @ModelView.setter
    def ModelView(self, value: 'AcadView'):
        pass

    @property
    def ShadePlot(self) -> acShadePlot:
        """Specifies the shaded viewport plotting mode of a viewport. """
        pass

    @ShadePlot.setter
    def ShadePlot(self, value: 'acShadePlot'):
        pass

    @property
    def SheetView(self) -> AcadView:
        """Returns and sets the sheet view associated with the viewport. """
        pass

    @SheetView.setter
    def SheetView(self, value: 'AcadView'):
        pass

    @property
    def SnapBasePoint(self) -> VARIANT:
        """
        Specifies the snap base point for the viewport.

        Returns: Variant (two-element array of doubles)
            A 2D WCS coordinate representing the snap base point for the viewport.

        """
        pass

    @SnapBasePoint.setter
    def SnapBasePoint(self, value: VARIANT):
        pass

    @property
    def SnapOn(self) -> bool:
        """Specifies the status of snap. """
        pass

    @SnapOn.setter
    def SnapOn(self, value: bool):
        pass

    @property
    def SnapRotationAngle(self) -> float:
        pass

    @SnapRotationAngle.setter
    def SnapRotationAngle(self, value: float):
        """Specifies the snap rotation angle of the viewport relative to the current UCS. """
        pass

    @property
    def StandardScale(self) -> acPlotScale | acViewportScale:
        """Specifies the standard scale for the layout, viewport, or plot configuration. """
        pass

    @StandardScale.setter
    def StandardScale(self, value: 'acPlotScale|acViewportScale'):
        pass

    @property
    def StandardScale2(self) -> float:
        """Specifies a standard scale for the viewport. """
        pass

    @StandardScale2.setter
    def StandardScale2(self, value: float):
        pass

    @property
    def Target(self) -> VARIANT:
        """
        Specifies the target point for the view or viewport.

        Returns: Variant (three-element array of doubles)

        """
        pass

    @Target.setter
    def Target(self, value: VARIANT):
        pass

    @property
    def TwistAngle(self) -> float:
        """Specifies the twist angle for the viewport."""
        pass

    @TwistAngle.setter
    def TwistAngle(self, value: float):
        pass

    @property
    def UCSIconAtOrigin(self) -> bool:
        """Specifies if the UCS icon is displayed at the origin. """
        pass

    @UCSIconAtOrigin.setter
    def UCSIconAtOrigin(self, value: bool):
        pass

    @property
    def UCSIconOn(self) -> bool:
        """Specifies if the UCS icon is on. """
        pass

    @UCSIconOn.setter
    def UCSIconOn(self, value: bool):
        pass

    @property
    def UCSPerViewport(self) -> bool:
        """Specifies if the UCS is saved with the viewport. """
        pass

    @UCSPerViewport.setter
    def UCSPerViewport(self, value: bool):
        pass

    @property
    def ViewportOn(self) -> bool:
        """Specifies the display status of the viewport. """
        pass

    @ViewportOn.setter
    def ViewportOn(self, value: bool):
        pass

    @property
    def VisualStyle(self) -> float:
        """
        Specifies the visual style for a viewport.

        Returns: ID of the visual style that should be assigned to the paper space viewport.

        """
        pass

    @VisualStyle.setter
    def VisualStyle(self, value: float):
        """Specifies the width of the object. """
        pass

    @property
    def Width(self) -> float:
        pass

    @Width.setter
    def Width(self, value: float):
        pass

    def Display(self, status: bool) -> None:
        """
        Toggles the display control of the PViewport object on or off.

        The display control must be on before the MSpace property can be used to activate the model space editing capabilities.
        Use the ViewportOn property to determine if a paper space viewport display has already been turned on with this method.

        Args:
            status: Boolean
                True: Viewport display is on.
                False: Viewport display is off.

        Returns:

        """
        pass

    def GetGridSpacing(self, XSpacing: float, YSpacing: float) -> None:
        """
        Gets the grid spacing for the viewport.

        Args:
            XSpacing: The X spacing of the grid in the viewport.
            YSpacing: The Y spacing of the grid in the viewport.

        Returns:

        """
        pass

    def GetSnapSpacing(self, XSpacing: float, YSpacing: float) -> None:
        """
        Gets the grid spacing for the viewport.

        Args:
            XSpacing: The snap spacing for the X axis.
            YSpacing: The snap spacing for the Y axis.

        Returns:

        """
        pass

    def SetGridSpacing(self, XSpacing: float, YSpacing: float) -> None:
        """
        Gets the grid spacing for the viewport.

        Args:
            XSpacing: The X spacing of the grid in the viewport.
            YSpacing: The Y spacing of the grid in the viewport.

        Returns:

        """
        pass

    def SetSnapSpacing(self, XSpacing: float, YSpacing: float) -> None:
        """
        Gets the grid spacing for the viewport.

        Args:
            XSpacing: The snap spacing for the X axis.
            YSpacing: The snap spacing for the Y axis.

        Returns:

        """
        pass

    def SyncModelView(self) -> None:
        """
        Updates the viewport parameters with the parameters in the associated model view.

        Returns:

        """
        pass


class AcadAttribute(IAcadEntity):
    pass


class AcadPolygonMesh(IAcadEntity):
    pass


class Acad3DFace(IAcadEntity):
    pass


class Acad3DSolid(IAcadEntity):
    pass


class AcadCircle(IAcadEntity):
    pass


class AcadBlockReference(IAcadEntity):
    """An instance of a block definition inserted into a drawing.  """

    @property
    def EffectiveName(self) -> str:
        """
        Specifies the original block name.

        The effective name is the name of the block as the user would see it in the user interface.
        Dynamic blocks may draw themselves with an anonymous block whose name is different than
        the block name the user sees for the block in the user interface.
        The Name property returns the name of the block used to draw the reference,
        while the EffectiveName is the name the user sees for the reference.

        """
        pass

    @property
    def HasAttributes(self) -> bool:
        """Specifies whether the block has any attributes in it. """
        pass

    @property
    def InsertionPoint(self) -> VARIANT:
        """
        Insertion point for a tolerance, text, block, or shape, and the origin (upper-left corner) of an OLE object.

        Returns: Variant (three-element array of doubles)

        """
        pass

    @property
    def InsUnits(self) -> str:
        """Specifies the insert units saved with the block. """
        pass

    @property
    def InsUnitsFactor(self) -> float:
        """Specifies the conversion factor between block units and drawing units. """
        pass

    @property
    def IsDynamicBlock(self) -> bool:
        """Specifies whether this is a dynamic block. """
        pass

    @property
    def Name(self) -> str:
        """Specifies the name of the object. """
        pass

    @Name.setter
    def Name(self, value: str):
        pass

    @property
    def Normal(self) -> VARIANT:
        """
        Specifies the three-dimensional normal unit vector for the object.

        Returns: Variant (three-element array of doubles)

        """
        pass

    @Normal.setter
    def Normal(self, value: VARIANT):
        pass

    @property
    def Rotation(self) -> float:
        """Specifies the rotation angle for the object. """
        pass

    @Rotation.setter
    def Rotation(self, value: float):
        pass

    @property
    def XEffectiveScaleFactor(self) -> float:
        """
        Specifies the effective XScale factor of the block.

        Returns: ACAD_NOUNITS, A non-zero real number.

        """
        pass

    @XEffectiveScaleFactor.setter
    def XEffectiveScaleFactor(self, value: float):
        pass

    @property
    def XScaleFactor(self) -> float:
        """Specifies the X scale factor for the block or external reference (xref). """
        pass

    @XScaleFactor.setter
    def XScaleFactor(self, value: float):
        pass

    @property
    def YEffectiveScaleFactor(self) -> float:
        """
        Specifies the effective YScale factor of the block.

        Returns: ACAD_NOUNITS, A non-zero real number.

        """
        pass

    @YEffectiveScaleFactor.setter
    def YEffectiveScaleFactor(self, value: float):
        pass

    @property
    def YScaleFactor(self) -> float:
        """Specifies the Y scale factor for the block or external reference (xref). """
        pass

    @YScaleFactor.setter
    def YScaleFactor(self, value: float):
        pass

    @property
    def ZEffectiveScaleFactor(self) -> float:
        """
        Specifies the effective ZScale factor of the block.

        Returns: ACAD_NOUNITS, A non-zero real number.

        """
        pass

    @ZEffectiveScaleFactor.setter
    def ZEffectiveScaleFactor(self, value: float):
        pass

    @property
    def ZScaleFactor(self) -> float:
        """Specifies the Z scale factor for the block or external reference (xref). """
        pass

    @ZScaleFactor.setter
    def ZScaleFactor(self, value: float):
        pass

    def ConvertToAnonymousBlock(self) -> None:
        """
        Converts a dynamic block to a regular anonymous block.

        The ComparedReference and ExternalReference objects inherit this method from BlockReference,
        but this method doesn't affect either of the object types when used.
        """
        pass

    def ConvertToStaticBlock(self, newBlockName: str) -> None:
        """
        Converts a dynamic block to a regular named block.

        Args:
            newBlockName: The name for the block.

        Returns: No return value.

        """
        pass

    def Explode(self) -> None:
        """
        Explodes the compound object into subentities.

        Depending on the type of compound object you are exploding, different results occur.
        Refer to the EXPLODE command topic in the AutoCAD Command Reference for a detailed list of explodable objects and their results.
        You do not have to explode a block in order to manipulate its constituent entities.

        All block definitions have an Item method that allow you to manipulate the entities within the block without exploding
        the block definition itself.

        The ComparedReference and ExternalReference objects inherit this method from BlockReference,
        but this method doesn't affect either of the object types when used.

        """
        pass

    def GetAttributes(self) -> Sequence[AcadAttributeReference]:
        """
        An object containing text that links to a block.

        """
        pass

    def GetConstantAttributes(self) -> Sequence['AcadAttribute']:
        """Gets the constant attributes in the block or external reference. """
        pass

    def GetDynamicBlockProperties(self) -> Sequence[AcadDynamicBlockReferenceProperty]:
        """Gets the properties of the dynamic block."""
        pass

    def ResetBlock(self) -> None:
        """Resets the dynamic block to the default state. """
        pass


class AcadHatch(IAcadEntity):
    pass


class AcadTolerance(IAcadEntity):
    pass


class AcadMtext(IAcadEntity):
    pass


class AcadMLeader(IAcadEntity):
    pass


class AcadLine(IAcadEntity):
    pass


class AcadLWPolyline(IAcadEntity):
    pass


class AcadMInsertBlock(AcadBlockReference):
    pass


class AcadExternalReference(AcadBlockReference):
    pass


class AcadMLine(IAcadEntity):
    pass


class AcadPolyfaceMesh(IAcadEntity):
    pass


class AcadPolyline(IAcadEntity):
    pass


class AcadRasterImage(IAcadEntity):
    pass


class AcadRay(IAcadEntity):
    pass


class AcadRegion(IAcadEntity):
    pass


class AcadSection(IAcadEntity):
    pass


class AcadSolid(IAcadEntity):
    pass


class AcadSpline(IAcadEntity):
    pass


class AcadTable(IAcadEntity):
    pass


class AcadText(IAcadEntity):
    pass


class AcadTrace(IAcadEntity):
    pass


class AcadXline(IAcadEntity):
    pass


class AcadEllipse(IAcadEntity):
    pass


class AcadArc(IAcadEntity):
    pass

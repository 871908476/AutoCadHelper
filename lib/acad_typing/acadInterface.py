from __future__ import annotations
from typing import TYPE_CHECKING, Any, Iterator, TypeVar, Collection, Sequence, overload
from win32com.client import VARIANT

if TYPE_CHECKING:
    from .acadEnums import acCmColor, acExtendOption
    from .acadCollections import AcadHyperlinks
    from .acadEnums import acLineWeight
    from .acadObjects import AcadLayer, AcadLinetype, AcadDictionary
    from .acadDocuments import AcadDocument
    from .acadApplication import AcadApplication


class IAcadInterface(object):
    """Acad 对象接口，实例属性被连接到原始对象"""

    def __init__(self, prototype) -> None:
        self.__prototype = prototype

    def __getattr__(self, attr):
        return getattr(self.__prototype, attr)

    @property
    def Prototype(self):
        return self.__prototype


class IAcadObject(IAcadInterface):
    """
    The standard interface for a basic AutoCAD object.
    """

    def Delete(self):
        pass

    def GetExtensionDictionary(self) -> AcadDictionary:
        """
        Gets the extension dictionary associated with an object.

        returns:
            Dictionary -- The extension dictionary for the object.

        """
        pass

    def GetXData(self, appName: str, xDataType: Sequence[int], xDataValue: Sequence[object]):
        """
        Gets the extended data (XData) associated with an object.
        """
        pass

    def SetXData(self, xDataType: Sequence[int], xDataValue: Sequence[object]):
        """
        Sets the extended data (XData) associated with an object.
        """
        pass

    @property
    def Application(self) -> AcadApplication:
        """Gets the Application object. """
        pass

    @property
    def Document(self) -> AcadDocument:
        '''Gets the document (drawing) in which the object belongs. '''
        return self.__document

    @property
    def Handle(self) -> str:
        '''Gets the handle of an object.  '''
        pass

    @property
    def HasExtensionDictionary(self) -> bool:
        """Determines whether the object has an extension dictionary associated with it."""
        pass

    @property
    def ObjectID(self) -> int:
        """Gets the object ID. """
        pass

    @property
    def ObjectName(self) -> str:
        '''Gets the AutoCAD class name of the object. '''
        return self.__objectName

    @property
    def OwnerID(self) -> int:
        '''Gets the object ID of the owner (parent) object. '''
        return self.__ownerID


T = TypeVar('T')


class IAcadCollection(IAcadInterface, Collection[T]):
    """
    集合类接口

    Args:
        IAcadInterface (_type_): 通用接口，提供原型对象 Prototype
        Collection (_type_): 集合泛型
    """

    def __init__(self, prototype):
        super().__init__(prototype)
        self.__index = -1

    def Pack(self, val) -> T:
        """
        提供 python 包装类

        Returns:
            T: 返回包装后的 python 实例对象
        """
        return val

    def __len__(self) -> int:
        return self.Prototype.Count

    def __contains__(self, __x: object) -> bool:
        for itm in self.Prototype:
            if __x == itm:
                return True
        return False

    def __iter__(self) -> Iterator[T]:
        return self

    def __next__(self):
        if self.__index == self.Prototype.Count - 1:
            raise StopIteration
        self.__index += 1
        print(self.__index)
        return self.Prototype.Item(self.__index)

    @overload
    def Add(self) -> T:
        pass

    @overload
    def Add(self, name: str, /) -> T:
        """
        Type: Dictionaries, DimStyles, Documents, Groups, Layers, Layouts, Linetypes, Materials, PopupMenus, RegisteredApplications, SelectionSets, TextStyles, Toolbars, Views, Viewports 
        Creates a member object and adds it to the appropriate collection.

        Returns:
            The newly added object.

        """
        pass

    @overload
    def Add(self, point: VARIANT, name: str) -> str:
        """
        Type: Blocks
        Creates a member object and adds it to the appropriate collection.

        Args:
            name: The name of the object to add to the collection.
            point (VARIANT(5 | 8192, (x,y,z))): The 3D WCS coordinates specifying where the Blocks object will be added.

        Returns:
            The name of the block to add to the collection..

        """
        pass

    @overload
    def Add(self, name: str, model_type: bool) -> T:
        """
        Type: PlotConfigurations
        Creates a member object and adds it to the appropriate collection.

        Args:
            name: The name of the object to add to the collection.
            model_type (bool):
                    True: The plot configuration applies only to the Model tab.
                    False: The plot configuration applies to all layouts.

        Returns:
            The newly added object.

        """
        pass

    @overload
    def Add(self, Name: str, Description: str, NamedLocation: VARIANT) -> T:
        """
        Type: Hyperlinks
        Creates a member object and adds it to the appropriate collection.

        Args:
            Name (str): The name of the hyperlink to add.
            Description (str): The description of the hyperlink to add.
            NamedLocation (VARIANT): A given location, such as a named view in AutoCAD or a bookmark in a word processing program.
                    If you specify a named view to jump to in an AutoCAD drawing, AutoCAD restores that view when the hyperlink is opened.

        Returns:
            T: The newly added object.
        """
        pass

    @overload
    def Add(self, Origin: VARIANT, XAxisPoint: VARIANT, YAxisPoint: VARIANT, Name: str) -> str:
        """
        Type: UCSs
        Creates a member object and adds it to the appropriate collection. 

        Args:
            Origin (VARIANT(5 | 8192, (x,y,z))): The 3D WCS coordinates specifying where the UCS is to be added.
            XAxisPoint (VARIANT(5 | 8192, (x,y,z))): The 3D WCS coordinates specifying where the UCS is to be added.
            YAxisPoint (VARIANT(5 | 8192, (x,y,z))): The 3D WCS coordinates specifying where the UCS is to be added.
            Name (str): The name of the UCS to add to the collection.

        Returns:
            The name of the UCS to add to the collection.
        """
        pass

    def Add(self, *args: Any, **kwargs: Any) -> Any:
        pass

    def Item(self, index: str | int) -> T:
        """
        Gets the member object at a given index in a collection, group, or selection set.

        Args:
            index: The index location in the collection for the member item to query.
                   The index must be either an integer or a string. If an integer, the index must be between 0 and N-1,
                   where N is the number of objects in the collection or selection set.

        Returns:
            The object at the given index location in the collection or selection set.

        """
        pass

    @property
    def Count(self):
        return self.Prototype.Count


class IAcadEntity(IAcadObject):
    """
    The standard interface for a basic AutoCAD entity.
    """

    @property
    def EntityTransparency(self) -> str:
        """Specifies the transparency value for the entity."""
        pass

    @EntityTransparency.setter
    def EntityTransparency(self, val: str):
        pass

    @property
    def Hyperlinks(self) -> AcadHyperlinks:
        pass

    @property
    def Layer(self) -> AcadLayer:
        pass

    @Layer.setter
    def Layer(self, value: AcadLayer):
        pass

    @property
    def Linetype(self) -> AcadLinetype:
        pass

    @Linetype.setter
    def Linetype(self, value: AcadLinetype):
        pass

    @property
    def LinetypeScale(self) -> float:
        """Specifies the linetype scale of an object. """
        pass

    @LinetypeScale.setter
    def LinetypeScale(self, value: float):
        pass

    @property
    def Lineweight(self) -> acLineWeight:
        pass

    @Lineweight.setter
    def Lineweight(self, value: acLineWeight):
        pass

    @property
    def Material(self) -> str:
        """Specifies the name of the material. """
        pass

    @Material.setter
    def Material(self, value: str):
        pass

    @property
    def PlotStyleName(self) -> str:
        pass

    @PlotStyleName.setter
    def PlotStyleName(self, value: str):
        pass

    @property
    def TrueColor(self) -> acCmColor:
        pass

    @TrueColor.setter
    def TrueColor(self, value: acCmColor):
        """Specifies the True Color of an object. """
        pass

    @property
    def Visible(self) -> bool:
        """Specifies the visibility of an object or the application. """
        pass

    @Visible.setter
    def Visible(self, value: bool):
        pass

    def ArrayPolar(self, NumberOfObjects: int, AngleToFill: float, CenterPoint: VARIANT) -> VARIANT:
        """
        Creates a polar array of objects given a NumberOfObjects, AngleToFill, and CenterPoint.
        Args:
            NumberOfObjects: The number of objects to be created in the polar array.
                This must be a positive integer greater than 1.
            AngleToFill: The angle to fill in radians. A positive value specifies counterclockwise rotation.
                A negative value specifies clockwise rotation. An error is returned for an angle that equals 0.
            CenterPoint: Variant (three-element array of doubles)
                The 3D WCS coordinates specifying the center point for the polar array.

        Returns: Variant (array of objects) , The array of newly created objects.

        """
        pass

    def ArrayRectangular(self, numberOfRows: int, numberOfColumns: int, numberOfLevels: int, distanceBwtnRows: float, distanceBwtnColumns: float,
                         distanceBwtnLevels: float) -> VARIANT:
        """
        Creates a 2D or 3D rectangular array of objects.
        Args:
            numberOfRows: The number of rows in the rectangular array.
                This must be a positive number. If this number is 1, then NumberOfColumns must be greater than 1.
            numberOfColumns: The number of columns in the rectangular array.
            numberOfLevels: The number of levels in a 3D array.
            distanceBwtnRows: The distance between the rows.
                If the distance between columns is a positive number, columns are added to the right of the base entity.
                If the distance is a negative number, columns are added to the left.
            distanceBwtnColumns: The distance between the columns.
            distanceBwtnLevels: The distance between the array levels.

        Returns: Variant (array of objects) , The array of newly created objects.

        """
        pass

    def Copy(self) -> object:
        """
        Duplicates the given object to the same location.

        Returns: The newly created duplicate object.

        """
        pass

    def GetBoundingBox(self, MinPoint: VARIANT, MaxPoint: VARIANT) -> None:
        """
        Gets two points of a box enclosing the specified object.
        Args:
            MinPoint: Variant (three-element array of doubles)
                The 3D WCS coordinates specifying the minimum point of the object's bounding box.
            MaxPoint: Variant (three-element array of doubles)

        """
        pass

    def Highlight(self, flag: bool) -> None:
        """
        Sets the highlight status for the given object, or for all objects in a given selection set.
        Args:
            flag: Boolean
                True: The object is highlighted.
                False: The existing highlight is removed from the object.

        """
        pass

    def IntersectWith(self, IntersectObject: object, ExtendOption: acExtendOption) -> VARIANT:
        """
        Gets the points where one object intersects another object in the drawing.
        Args:
            IntersectObject: The object can be one of the supported drawing objects or an AttributeReference
            ExtendOption: This option specifies if none, one or both, of the objects are to be extended in order to attempt an intersection.

        Returns: Variant (array of doubles)
            The array of points where one object intersects another object in the drawing.


        """
        pass

    def Mirror(self, Point1: VARIANT, Point2: VARIANT) -> object:
        """
        Creates a mirror-image copy of a planar object around an axis.

        Args:
            Point1: Variant (three-element array of doubles)
                The 3D WCS coordinates specifying the first point of the mirror axis.
            Point2:Variant (three-element array of doubles)
                The 3D WCS coordinates specifying the first point of the mirror axis.

        Returns: This object can be one of any drawing object and is the result of mirroring the original object.

        """
        pass

    def Mirror3D(self, Point1: VARIANT, Point2: VARIANT, Point3: VARIANT) -> object:
        """
        Creates a mirror image of the given object about a plane.

        Args:
            Point1: Variant (three-element array of doubles)
                The 3D WCS coordinates specifying the first point of the mirror axis.
            Point2: Variant (three-element array of doubles)
                The 3D WCS coordinates specifying the first point of the mirror axis.
            Point3: Variant (three-element array of doubles)
                The 3D WCS coordinates specifying the first point of the mirror axis.

        Returns: This object can be one of any drawing object and is the result of mirroring the original object.

        """
        pass

    def Move(self, Point1: VARIANT, Point2: VARIANT) -> None:
        """
        Moves an object along a vector.

        Args:
            Point1: Variant (three-element array of doubles)
            Point2: Variant (three-element array of doubles)

        """
        pass

    def Rotate(self, BasePoint: VARIANT, RotationAngle: float) -> None:
        """
        Rotates an object around a base point.

        Args:
            BasePoint: Variant (three-element array of doubles)
            RotationAngle: The angle in radians to rotate the object.
                This angle determines how far an object rotates around the base point relative to its current location.

        Returns:

        """
        pass

    def Rotate3D(self, Point1: VARIANT, Point2: VARIANT, RotationAngle: float) -> None:
        """
        Rotates an object around a 3D axis. Point1 and Point2 define the line that becomes the axis of rotation.
        Args:
            Point1: Variant (three-element array of doubles)
            Point2: Variant (three-element array of doubles)
                The 3D WCS coordinates specifying the first point of the axis line.
            RotationAngle: The angle in radians to rotate the object about the selected axis.

        """
        pass

    def ScaleEntity(self, BasePoint: VARIANT, ScaleFactor: float) -> None:
        """
        Rotates an object around a base point.

        Args:
            BasePoint: Variant (three-element array of doubles)
                The 3D WCS coordinates specifying the base point.
            ScaleFactor: The factor by which to scale the object.
                The dimensions of the object are multiplied by the scale factor.
                A scale factor greater than 1 enlarges the object.
                A scale factor between 0 and 1 reduces the object.
                The scale factor must be greater than 0.0.

        Returns:

        """
        pass

    def TransformBy(self, TransformationMatrix: VARIANT) -> None:
        """
        Moves, scales, or rotates an object given a 4x4 transformation matrix.

        This method will return an error if the transformation matrix is not correct.

        The following table demonstrates the transformation matrix configuration,
            where R = Rotation, and T = Translation: R00

            R00  R01  R02  T0
            R10  R11  R12  T1
            R20  R21  R22  T2
            0    0    0    1


        Args:
            TransformationMatrix: Variant (4x4 array of doubles)
                A 4x4 matrix specifying the transformation to perform.

        Returns:

        """
        pass

    def Update(self) -> None:
        """
        Updates the object to the drawing screen.

        Returns:

        """
        pass

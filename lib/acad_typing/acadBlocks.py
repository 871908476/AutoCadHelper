from __future__ import annotations
from .acadInterface import IAcadCollection, IAcadObject, IAcadInterface
from win32com.client import VARIANT
from typing import TYPE_CHECKING, Iterator

if TYPE_CHECKING:
    from .acadObjects import AcadLayout
    from .acadDimensions import *
    from .acadEntities import *
    from .acadEnums import *
    from .acadDocuments import AcadDatabase


class AcadBlock(IAcadObject):
    """A block definition containing a name and a set of objects. """

    def __iter__(self) -> Iterator[IAcadObject]:
        pass

    def Add3DFace(self, point1: VARIANT, point2: VARIANT, point3: VARIANT,
                  point4: VARIANT) -> Acad3DFace:
        """
        Creates a 3DFace object given four vertices

        Args:
            point1 (VARIANT(5|8192)):  Variant (three-element array of doubles) 
            point2 (VARIANT(5|8192)):  Variant (three-element array of doubles) 
            point3 (VARIANT(5|8192)):  Variant (three-element array of doubles) 
            point4 (VARIANT(5|8192)):  Variant (three-element array of doubles) 
        """
        pass

    def Add3DMesh(self, M: int, N: int, points_matrix: VARIANT) -> AcadPolygonMesh:
        """
        Creates a free-form 3D mesh, given the number of points in the M and N directions and the coordinates of the points in the M and N directions.

        Args:
            M (int): Dimensions of the point array. The size of the mesh in both the M and N directions is limited to between 2 and 256.
            N (int): Dimensions of the point array. The size of the mesh in both the M and N directions is limited to between 2 and 256.
            points_matrix (VARIANT): M x N matrix of 3D WCS coordinates. Defining vertices begins with vertex (0,0).
                Supplying the coordinate locations for each vertex in row M must be done before specifying vertices in row M + 1.
        """
        pass

    def Add3Dpoly(self, points_array: VARIANT) -> None:
        """
        Creates a 3D polyline from the given array of coordinates. 
        To close the polyline, use the Closed property on the 3DPolyline object.

        Args:
            points_array (VARIANT):  Variant (array of doubles). 
            An array of 3D WCS coordinates. 
            The polyline will be created according to the order of the coordinates in the array. The number of elements in the array must be a multiple of three. 
            (Three elements define a single coordinate.) 

        """
        pass

    def AddArc(self, center: VARIANT, radius: float, startangle: float, endangle: float) -> None:
        """
        Creates an arc given the center, radius, start angle, and end angle of the arc. 

        Args:
            center (VARIANT): Variant (three-element array of doubles) 
            radius (float): The radius of the arc
            startangle (float): The start and end angles, in radians, defining the arc. A start angle greater than an end angle defines a counterclockwise arc.
            endangle (float): The start and end angles, in radians, defining the arc. A start angle greater than an end angle defines a counterclockwise arc.
        """
        pass

    def AddAttribute(self, height: float, mode: int, prompt: str, insertion_point: VARIANT,
                     tag: str, value: str) -> AcadAttribute:
        """
        Creates an attribute definition at the given location with the specified properties. 
        
        An attribute definition is associated to the block for which it is created. 
        Attribute definitions created in model space or paper space are not considered to be attached to any given block. 
        The AutoCAD AFLAGS system variable stores the mode setting. You can query this value using the GetVariable method, or set it using the SetVariable method. 


        Args:
            height (float): The text height in the current drawing unit.
            mode (int): AcAttributeMode enum 
                Any combination of constants can be used by adding them together: 
                    acAttributeModeInvisible: Specifies that attribute values will not appear when you insert the block. The AutoCAD ATTDISP command overrides the Invisible mode. 
                    acAttributeModeConstant: Gives attributes a fixed value for block insertions. 
                    acAttributeModeVerify: Prompts to verify the attribute value is correct when the block is inserted. 
                    acAttributeModeLockPosition: Locks the position of the attributes. 
                    acAttributeModeMultipleLine: Allows the attributes to carry-over onto multiple lines. Prompts you to verify that the attribute value is correct when you insert the block. 
                    acAttributeModePreset: Sets the attribute to its default value when you insert a block containing a current attribute. The value cannot be edited in this mode. 
            prompt (str): This string appears when a block containing this attribute is inserted. The default for this string is the Tag string. 
                Inputting acAttributeModeConstant for the Mode parameter disables the prompt. 
            insertion_point (VARIANT):  Variant (three-element array of doubles)  The 3D WCS coordinates specifying the location for the attribute. 
            tag (str): This non-null string identifies each occurrence of the attribute. 
                Enter any characters except spaces or exclamation points. AutoCAD changes lowercase letters to uppercase.
            value (str): This non-null string is the default attribute value. 
        """
        pass

    def AddBox(self, origin: VARIANT, length: float, width: float, height: float) -> Acad3DSolid:
        """
        A solid object with free-form surface support. 

        Args:
            origin (VARIANT): Variant (three-element array of doubles) 
                The 3D WCS coordinates specifying the origin of the box. This coordinate represents the center of the bounding box for the object, not a corner. 
            length (float): The length of the box. Must be a positive number.
            width (float): The width of the box. Must be a positive number. 
            height (float): The height of the box. Must be a positive number.

        Returns:
            Acad3DSolid: A 3DSolid object as the newly created box.
        """
        pass

    def AddCircle(self, center: VARIANT, radius: float) -> AcadCircle:
        """
        Creates a circle given a center point and radius. 

        Args:
            center (VARIANT): Variant (three-element array of doubles) 
            radius (float): The radius of the circle. Must be a positive number.
        """
        pass

    def AddCone(self, center: VARIANT, base_radius: float, height: float) -> Acad3DSolid:
        """
        Creates a 3D solid cone with the base on the XY plane of the WCS

        Args:
            center (VARIANT):  Variant (three-element array of doubles) 
            base_radius (float): The radius of the cone base. Must be a positive number. 
            height (float): The height of the cone. Must be a positive number.
        """
        pass

    def AddCustomObject(self, class_name: str) -> object:
        """
        Creates a custom object. 

        Args:
            class_name (str): The rxClassName must be defined in an ObjectARX® application (ObjectARX DLL) or the method will fail. 

        """
        pass

    def AddCylinder(self, center: VARIANT, radius: float, height: float) -> Acad3DSolid:
        """
        Creates a 3D solid cylinder whose base is on the XY plane of the WCS.

        Args:
            center (VARIANT): Variant (three-element array of doubles) 
            radius (float): The cylinder radius. Must be a positive number.
            height (float): The cylinder height. Must be a positive number. 

        """
        pass

    def AddDim3PointAngular(self, angle_vertex: VARIANT, first_end_point: VARIANT,
                            second_end_point: VARIANT, text_point: VARIANT) -> AcadDim3PointAngular:
        """
        Creates an angular dimension using 3 points. 

        Args:
            angle_vertex (VARIANT): Variant (three-element array of doubles) 
            first_end_point (VARIANT): Variant (three-element array of doubles) 
            second_end_point (VARIANT): Variant (three-element array of doubles) 
            text_point (VARIANT): Variant (three-element array of doubles) 
        """
        pass

    def AddDimAligned(self, ext_line1_point: VARIANT, ext_line2_point: VARIANT,
                      text_position: VARIANT) -> AcadDimAligned:
        """
        Creates an aligned dimension object. 

        Args:
            ext_line1_point (VARIANT): Variant (three-element array of doubles) 
            ext_line2_point (VARIANT): Variant (three-element array of doubles) 
            text_position (VARIANT): Variant (three-element array of doubles) 
        """
        pass

    def AddDimAngular(self, AngleVertex: VARIANT, FirstEndPoint: VARIANT, SecondEndPoint: VARIANT,
                      TextPoint: VARIANT) -> AcadDimAngular:
        """
        Creates an angular dimension for an arc, two lines, or a circle. 

        Args:
            AngleVertex (VARIANT): Variant (three-element array of doubles) 
                The 3D WCS coordinates specifying the center of the circle or arc, or the common vertex between the two dimensioned lines. 
            FirstEndPoint (VARIANT): Variant (three-element array of doubles) 
            SecondEndPoint (VARIANT): Variant (three-element array of doubles) 
            TextPoint (VARIANT): Variant (three-element array of doubles) 
        """
        pass

    def AddDimArc(self, ArcCenter: VARIANT, FirstEndPoint: VARIANT, SecondEndPoint: VARIANT,
                  ArcPoint: VARIANT) -> AcadDimArcLength:
        """
        Creates an arc length dimension for an arc. 

        Args:
            ArcCenter (VARIANT): Variant (three-element array of doubles) 
            FirstEndPoint (VARIANT): Variant (three-element array of doubles) 
            SecondEndPoint (VARIANT): Variant (three-element array of doubles) 
            ArcPoint (VARIANT): Variant (three-element array of doubles) 
        """
        pass

    def AddDimDiametric(self, ChordPoint: VARIANT, FarChordPoint: VARIANT,
                        LeaderLength: float) -> AcadDimDiametric:
        """
        _summary_

        Args:
            ChordPoint (VARIANT): Variant (three-element array of doubles)
                The 3D WCS coordinates specifying the first diameter point on the circle or arc. 
            FarChordPoint (VARIANT): Variant (three-element array of doubles)
                The 3D WCS coordinates specifying the second diameter point on the circle or arc. 
            LeaderLength (float): The positive value representing the length from the ChordPoint to the annotation text or dogleg
        """
        pass

    def AddDimOrdinate(self, DefinitionPoint: VARIANT, LeaderEndPoint: VARIANT,
                       UseXAxis: bool) -> AcadDimOrdinate:
        """
        Creates an ordinate dimension given the definition point and the leader endpoint. 

        Args:
            DefinitionPoint (VARIANT):  Variant (three-element array of doubles) 
                The 3D WCS coordinates specifying the point to be dimensioned.
            LeaderEndPoint (VARIANT):  Variant (three-element array of doubles) 
                The 3D WCS coordinates specifying the endpoint of the leader. This will be the location at which the dimension text is displayed. 
            UseXAxis (bool): 
                True: Creates an ordinate dimension displaying the X axis value. 
                False: Creates an ordinate dimension displaying the Y axis value. 
        """
        pass

    def AddDimRadial(self, Center: VARIANT, ChordPoint: VARIANT,
                     LeaderLength: float) -> AcadDimRadial:
        """
        A dimension measuring the radius of a circle or arc. 

        Args:
            Center (VARIANT): Variant (three-element array of doubles) 
            ChordPoint (VARIANT): Variant (three-element array of doubles) 
            LeaderLength (float): The positive value representing the length from the ChordPoint to the annotation text or dogleg.
        """
        pass

    def AddDimRadialLarge(self, Center: VARIANT, ChordPoint: VARIANT, OverrideCenter: VARIANT,
                          JogPoint: VARIANT, JogAngle: float) -> AcadDimRadialLarge:
        """
        Creates a jogged radial dimension for an arc, circle, or polyline arc segment.

        Args:
            Center (VARIANT): Variant (three-element array of doubles) 
                The 3D WCS coordinates specifying the center of the arc, circle, or polyline arc segment. 
            ChordPoint (VARIANT): Variant (three-element array of doubles) 
                The 3D WCS coordinates specifying the chord point for the arc.
            OverrideCenter (VARIANT): Variant (three-element array of doubles) 
                The 3D WCS coordinates specifying the override center location or pick point.
            JogPoint (VARIANT): Variant (three-element array of doubles) 
                The 3D WCS coordinates specifying the jog location or pick point. 
            JogAngle (float): The value for the jog angle.
                The value for the jog angle.
        """
        pass

    def AddDimRotated(self, XLine1Point: VARIANT, XLine2Point: VARIANT, DimLineLocation: VARIANT,
                      RotationAngle: float) -> AcadDimRotated:
        """
        Creates a rotated linear dimension

        Args:
            XLine1Point (VARIANT): Variant (three-element array of doubles) 
                The 3D WCS coordinates specifying the first end of the linear dimension to be measured. This is where the first extension line will be attached. 
            XLine2Point (VARIANT): Variant (three-element array of doubles) 
                The 3D WCS coordinates specifying the second end of the linear dimension to be measured. This is where the second extension line will be attached.
            DimLineLocation (VARIANT): Variant (three-element array of doubles) 
                The 3D WCS coordinates specifying a point on the dimension line. This will define the placement of the dimension line and the dimension text.
            RotationAngle (float): The angle, in radians, of rotation displaying the linear dimension.
        """
        pass

    def AddEllipse(self, Center: VARIANT, MajorAxis: VARIANT, RadiusRatio: float) -> AcadEllipse:
        """
        Creates an ellipse in the XY plane of the WCS given the center point, a point on the major axis, and the radius ratio.

        Args:
            Center (VARIANT): Variant (three-element array of doubles) 
                The 3D WCS coordinates specifying the center of the ellipse. 
            MajorAxis (VARIANT): Variant (double) 
                A positive value defining the length of the major axis of the ellipse. 
            RadiusRatio (float): _description_
                A positive value defining the major to minor axis ratio of an ellipse. A radius ratio of 1.0 defines a circle. 
        """
        pass

    def AddEllipticalCone(self, Center: VARIANT, MajorRadius: float, MinorRadius: float,
                          Height: float) -> Acad3DSolid:
        """
        Creates a 3D solid elliptical cone on the XY plane of the WCS given the Center, MajorRadius, MinorRadius, and Height.

        Args:
            Center (VARIANT): Variant (three-element array of doubles) 
                The 3D WCS coordinates specifying the center of the bounding box.
            MajorRadius (float): The length of the major radius for the ellipse base. Must be a positive number.
            MinorRadius (float): The length of the minor radius for the ellipse base. Must be a positive number.
            Height (float): The height of the cone. Must be a positive number.

        """
        pass

    def AddEllipticalCylinder(self, Center: VARIANT, MajorRadius: float, MinorRadius: float,
                              Height: float) -> Acad3DSolid:
        """
        Creates a 3D solid elliptical cylinder whose base is on the XY plane of the WCS, given the Center, MajorRadius, MinorRadius, and Height.

        Args:
            Center (VARIANT): Variant (three-element array of doubles) 
                The 3D WCS coordinates specifying the center of the bounding box.
            MajorRadius (float): The length of the major radius for the ellipse base. Must be a positive number.
            MinorRadius (float): The length of the minor radius for the ellipse base. Must be a positive number.
            Height (float): The height of the cone. Must be a positive number.

        """
        pass

    def AddExtrudedSolid(self, Profile: 'AcadRegion', Height: float,
                         TaperAngle: float) -> Acad3DSolid:
        """
        Creates an extruded solid given the profile, height, and taper angle. 
        
        Tapered extrusions are possible only with loops that are continuous at the vertices.
        A large taper angle or long extrusion height can cause the object, or portions of the object, to intersect with itself before reaching the extrusion height.
        AutoCAD does not allow an extrusion when the resulting solid intersects with itself. 

        Args:
            Profile (AcadRegion): A profile can only be a Region object. 
            Height (float): The height of the extrusion along the Z axis of the object's coordinate system.
                If you enter a positive number, AutoCAD extrudes the object along the positive Z axis.
                If you enter a negative number, AutoCAD extrudes the object along the negative Z axis.
            TaperAngle (float): The taper angle of the extrusion must be provided in radians. The range of the taper angle is from -90 to +90 degrees. 
                Positive angles taper in from the base, negative angles taper out. The default angle, 0, extrudes a 2D object perpendicular to its plane. 



        Returns:
            Acad3DSolid: A 3DSolid object as the newly created extruded solid.
        """
        pass

    def AddExtrudedSolidAlongPath(
            self, Profile: 'AcadRegion',
            Path: 'AcadArc|AcadCircle|AcadEllipse|AcadPolyline|AcadSpline ') -> Acad3DSolid:
        """
        _summary_

        Args:
            Profile (AcadRegion): A profile can only be a Region object.
            Path (AcadArc|AcadCircle|AcadEllipse|AcadPolyline|AcadSpline ): The path can only be a Polyline, Circle, Ellipse, Spline, or Arc object.

        Returns:
            Acad3DSolid: The extruded 3DSolid object.
        """
        pass

    def AddHatch(self, PatternType: 'int|acPatternType|acGradientPatternType', PatternName: str,
                 Associativity: bool, HatchObjectType: 'int|acHatchObjectType') -> AcadHatch:
        """
        Creates a Hatch object. 

        Args:
            PatternType (int):  AcPatternType or AcGradientPatternType enum 
                If the HatchObjectType parameter value is acHatchObject, then use the AcPatternType enum;
                if the HatchObjectType parameter value is AcGradientObject, then use the AcGradientPatternType enum. 
                    
            PatternName (str): If the HatchObjectType parameter value is acHatchObject, then PatternName should contain the hatch pattern name.
                If the HatchObjectType parameter value is acGradientObject, then PatternName should contain one of the gradient pattern names listed in GradientName. 
            Associativity (bool): 
                True: The hatch will be associative. 
                False: The hatch will not be associative.       
            HatchObjectType (int): AcHatchObjectType enum 
                The default value is the AcHatchObjectType enum value of AcHatchObject. 
                If the AcHatchObjectType enum value is AcGradientObject, then PatternType should be of type AcGradientPatternType, 
                and PatternName should contain the gradient pattern name.

        Returns:
            AcadHatch: The newly created Hatch object. 

        """
        pass

    def AddLeader(self, PointsArray: VARIANT,
                  Annotation: 'AcadBlockReference|AcadMtext|AcadTolerance',
                  Type: 'acLeaderType') -> AcadMLeader:
        """
        Creates a leader line based on the provided coordinates or adds a new leader cluster to the MLeader object. 


        Args:
            PointsArray (VARIANT): Variant (array of doubles) 
                The array of 3D WCS coordinates specifying the leader. You must provide at least two points to define the leader. The third point is optional. 
            Annotation (AcadBlockReference|AcadMtext|AcadTolerance): The object that should be attached to the leader. The value can also be NULL to not attach an object.tion_
            Type (AcLeaderType): _description_
        """
        pass

    def AddLightWeightPolyline(self, VerticesList: VARIANT) -> AcadLWPolyline:
        """
        Creates a lightweight polyline from a list of vertices.
        
        The vertices specify the endpoints for the line segments that make up the polyline. To add an arc segment, 
        first create the polyline with all line segments, and then add a bulge to the individual segments you want to be arcs. 
        To add a bulge value to a segment, use the SetBulge method. 
        The elevation for the polyline will be set at the current elevation for the layout. 
        Use the ElevationModelspace or ElevationPaperspace property to determine the elevation for the polyline. 
        Coordinates can be converted to and from the OCS using the TranslateCoordinates method


        Args:
            VerticesList (VARIANT): Variant (array of doubles) 
                The array of 2D OCS coordinates specifying the vertices of the polyline.
                At least two points (four elements) are required for constructing a lightweight polyline. The array size must be a multiple of 2. 

        """
        pass

    def AddLine(self, StartPoint: VARIANT, EndPoint: VARIANT) -> AcadLine:
        """
        Creates a line passing through two points.

        Args:
            StartPoint (VARIANT): Variant (three-element array of doubles) 
            EndPoint (VARIANT): Variant (three-element array of doubles) 
        """
        pass

    def AddMInsertBlock(self,
                        InsertionPoint: VARIANT,
                        Name: str,
                        XScale: float,
                        YScale: float,
                        ZScale: float,
                        Rotation: float,
                        NumRows: int,
                        NumColumns: int,
                        RowSpacing: float,
                        ColumnSpacing: float,
                        Password: VARIANT = None) -> AcadMInsertBlock:
        """
        Inserts an array of blocks.

        Args:
            InsertionPoint (VARIANT): Variant (three-element array of doubles)
            Name (str): The name of the MInsertBlock
                You cannot precede the name of an MInsertBlock with an asterisk to separate the block's objects during insertion, as you can with a standard Block.
            XScale (float): The X scale factor.
            YScale (float): The Y scale factor.
            ZScale (float): The Z scale factor.
            Rotation (float): The rotation angle in radians.
            NumRows (int): A positive integer representing the number of rows for the array.
            NumColumns (int): A positive integer representing the number of columns for the array.
            RowSpacing (float): The distance between the array rows.
            ColumnSpacing (float): The distance between the array columns.
            Password (VREPRINT): The password that is required to open and insert the drawing.
        """
        pass

    def AddMLeader(self, pointsArray: VARIANT, leaderLineIndex: int) -> AcadMLeader:
        """
        Creates an mleader line, given coordinates.

        Args:
            pointsArray (VARIANT): Variant (three-element array of Doubles) 
                The array of 3D WCS coordinates specifying the leader. You must provide at least two point to define the leader. The third point is optional.
            leaderLineIndex (int): Input index of the mleader cluster
        """
        pass

    def AddMLine(self, VertexList: VARIANT) -> AcadMLine:
        """
        Creates multiple lines passing through an array of points.

        Args:
            VertexList (VARIANT): Variant (array of doubles) 
                An array of the 3D WCS coordinates specifying the vertices for the multiline.
        """
        pass

    def AddMText(self, InsertionPoint: VARIANT, Width: float, Text: str) -> AcadMtext:
        """
        Creates an MText entity in a rectangle defined by the insertion point and width of the bounding box.

        Args:
            InsertionPoint (VARIANT): Variant (three-element array of doubles) 
            Width (float): The width of the MText bounding box. 
            Text (str): The actual text string for the MText object. 
        """
        pass

    def AddPoint(self, point: VARIANT) -> AcadPoint:
        """
        Creates a Point object at a given location.

        Args:
            point (VARIANT): Variant (three-element array of doubles) 
        """
        pass

    def AddPolyfaceMesh(self, VerticesList: VARIANT, FaceList: VARIANT) -> AcadPolyfaceMesh:
        """
        Creates a polyface mesh from a list of vertices.

        Args:
            VerticesList (VARIANT): Variant (array of doubles) 
                An array of 3D WCS coordinates used to create the polyface mesh vertices. 
                At least four points (twelve elements) are required for constructing a polyface mesh object. 
                The array size must be a multiple of three.
            FaceList (VARIANT): Variant (array of integers)
                An array of integers representing the vertex numbers for each face.
                Faces are defined in groups of four vertex index values, so the size of this array must be a multiple of four.
        """
        pass

    def AddPolyline(self, VerticesList: VARIANT) -> AcadPolyline:
        """
        Creates a polyline from a list of vertices.

        Args:
            VerticesList (VARIANT): Variant (array of doubles) 
                An array of OCS coordinates used to create the polyline vertices. 
                Each vertex is represented with three elements, with the first two being the X and Y coordinates in OCS; the third element is ignored. 
                At least two points (six elements) are required for constructing a polyline object. 
                The array size must be a multiple of three.

        """
        pass

    def AddRaster(self, ImageFileName: str, InsertionPoint: VARIANT, ScaleFactor: float,
                  RotationAngle: float) -> AcadRasterImage:
        """
        Creates a new raster image based on an existing image file.

        Args:
            ImageFileName (str): The full path and file name of the image.
            InsertionPoint (VARIANT): Variant (three-element array of doubles) 
                The 3D WCS coordinates in the drawing where the raster image will be created. 
            ScaleFactor (float): The raster image scale factor. The default image scale factor is 1. 
                The scale factor must be a positive number. You can set the scale of the image to the scale of the geometry created in the AutoCAD drawing.
            RotationAngle (float): The rotation angle in radians for the raster image. 
        """
        pass

    def AddRay(self, Point1: VARIANT, Point2: VARIANT) -> AcadRay:
        """
        Creates a ray passing through two unique points.

        Args:
            Point1 (VARIANT): Variant (three-element array of doubles) 
            Point2 (VARIANT): Variant (three-element array of doubles) 
        """
        pass

    def AddRegion(self, ObjectList: VARIANT) -> None:
        """
        Creates a region from a set of entities. The given entities must form a closed coplanar region.

        Args:
            ObjectList (VARIANT): Variant (array of Arc, Circle, Ellipse, Line, LWPolyline, Spline objects) 
                The array of objects forming the closed coplanar face to be made into a region. 
        """
        pass

    def AddRevolvedSolid(self, Profile: 'AcadRegion', AxisPoint: VARIANT, AxisDir: VARIANT,
                         Angle: float) -> Acad3DSolid:
        """
        Creates a revolved solid, given the region around an axis.

        Args:
            Profile (AcadRegion): A profile can only a Region object. 
            AxisPoint (VARIANT): Variant (three-element array of doubles) 
            AxisDir (VARIANT): Variant (three-element array of doubles) 
            Angle (float): The angle of revolution in radians. Enter 6.28 for a full circle revolution. 

        Returns:
            Acad3DSolid: A 3DSolid object as the newly created revolved solid. 

        """
        pass

    def AddSection(self, FromPoint: VARIANT, ToPoint: VARIANT, planeVector: VARIANT) -> AcadSection:
        """
        Creates a section plane. 

        Args:
            FromPoint (VARIANT): The 3D WCS coordinates specifying the finite start point of the section. 
            ToPoint (VARIANT): The 3D WCS coordinates specifying a point through which the section will pass. 
                The section extends from FromPoint, through ToPoint to infinity. 
            planeVector (VARIANT): A 3D directional vector specifying the direction of the section plane

        Returns:
            AcadSection: The newly created Section object.
        """
        pass

    def AddShape(self, Name: str, InsertionPoint: VARIANT, ScaleFactor: float,
                 Rotation: float) -> IAcadEntity:
        """
        Creates a Shape object based on a template identified by name, at the given insertion point, scale factor, and rotation.

        Args:
            Name (str): The name of the shape to insert
            InsertionPoint (VARIANT): Variant (three-element array of doubles) 
            ScaleFactor (float): The scale factor to be applied to the shape. Use 1.0 to specify no scale. Must be a positive number
            Rotation (float): The angle of rotation in radians to be applied to the shape. 

        Returns:
            IAcadEntity: The newly created Shape object. 
        """
        pass

    def AddSolid(self, Point1: VARIANT, Point2: VARIANT, Point3: VARIANT,
                 Point4: VARIANT) -> AcadSolid:
        """
        Creates a 2D solid polygon.

        Args:
            Point1 (VARIANT): Variant (three-element array of doubles) 
            Point2 (VARIANT): Variant (three-element array of doubles) 
            Point3 (VARIANT): Variant (three-element array of doubles) 
            Point4 (VARIANT): Variant (three-element array of doubles) 

        Returns:
            AcadSolid: The newly created polygon.
        """
        pass

    def AddSphere(self, Center: VARIANT, Radius: float) -> Acad3DSolid:
        """
        Creates a sphere given the center and radius.

        Args:
            Center (VARIANT): Variant (three-element array of doubles) 
            Radius (float): The radius of the sphere. Must be a positive number. 

        Returns:
            Acad3DSolid: A 3DSolid object as the newly created sphere.
        """
        pass

    def AddSpline(self, PointsArray: VARIANT, StartTangent: VARIANT,
                  EndTangent: VARIANT) -> AcadSpline:
        """
        Creates a quadratic or cubic NURBS (nonuniform rational B-spline) curve.

        Args:
            PointsArray (VARIANT): Variant (three-element array of doubles) 
            StartTangent (VARIANT): Variant (three-element array of doubles) 
            EndTangent (VARIANT): Variant (three-element array of doubles) 

        Returns:
            AcadSpline: The newly created Spline object.
        """
        pass

    def AddTable(self, InsertionPoint: VARIANT, NumRows: int, NumColumns: int, RowHeight: float,
                 ColWidth: float) -> AcadTable:
        """
        Adds a table to a drawing.

        Args:
            InsertionPoint (VARIANT): Variant (three-element array of doubles) 
            NumRows (int): The number of rows in the table.
            NumColumns (int): The number of columns in the table.
            RowHeight (float): The height of the rows in the table.
            ColWidth (float): The width of the columns in the table.

        Returns:
            AcadTable: The newly created table object.
        """
        pass

    def AddText(self, TextString: str, InsertionPoint: VARIANT, Height: float) -> AcadText:
        """
        Creates a single line of text. 

        Args:
            TextString (str): The actual text to be displayed
            InsertionPoint (VARIANT): Variant (three-element array of doubles)
            Height (float): The height of the text. Must be a positive number.

        Returns:
            AcadText: The newly created Text object.
        """
        pass

    def AddTolerance(self, Text: str, InsertionPoint: VARIANT, Direction: VARIANT) -> AcadTolerance:
        """
        Creates a tolerance entity.

        Args:
            Text (str): The text string for the tolerance.
            InsertionPoint (VARIANT): Variant (three-element array of doubles) 
            Direction (VARIANT): Variant (three-element array of doubles) 

        Returns:
            AcadTolerance: The newly created Tolerance object.
        """
        pass

    def AddTorus(self, Center: VARIANT, TorusRadius: float, TubeRadius: float) -> Acad3DSolid:
        """
        Creates a torus at the given location. 

        Args:
            Center (VARIANT): Variant (three-element array of doubles)
            TorusRadius (float): The distance from the center of the torus to the center of the tube. Must be a positive number.
            TubeRadius (float): The radius of the tube. Must be a positive number. 

        Returns:
            Acad3DSolid: A 3DSolid object as the newly created torus.
        """
        pass

    def AddTrace(self, PointsArray: VARIANT) -> AcadTrace:
        """
        Creates a Trace object from an array of points. 
        
        The endpoints of a trace are always on the centerline and are always cut square. AutoCAD automatically calculates the correct bevels for connection to adjacent trace segments. 

        Traces are solid filled when the Fill mode is on. When Fill mode is off, only the outline of a trace appears. 

        To set the Fill mode, use the AutoCAD FILLMODE system variable. The AutoCAD TRACEWID system variable stores the current width used for Trace objects.


        Args:
            PointsArray (VARIANT): Variant (array of doubles)

        Returns:
            AcadTrace: The newly created Trace object.
        """
        pass

    def AddWedge(self, Center: VARIANT, Length: float, Width: float, Height: float) -> Acad3DSolid:
        """
        Creates a wedge with edges parallel to the axes given the length, width, and height.

        Args:
            Center (VARIANT): Variant (three-element array of doubles)
            Length (float): The length of the wedge corresponding to the X axis. Must be a positive number. 
            Width (float): The width of the wedge corresponding to the Y axis. Must be a positive number.
            Height (float): The height of the wedge corresponding to the Z axis. Must be a positive number.

        Returns:
            Acad3DSolid: A 3DSolid object as the newly created wedge
        """
        pass

    def AddXline(self, Point1: VARIANT, Point2: VARIANT) -> AcadXline:
        """
        A construction line that is infinite in both directions. 

        Args:
            Point1 (VARIANT): Variant (three-element array of doubles) 
            Point2 (VARIANT): Variant (three-element array of doubles) 

        Returns:
            AcadXline: The newly created XLine object.
        """
        pass

    def AttachExternalReference(self,
                                PathName: str,
                                Name: str,
                                InsertionPoint: VARIANT,
                                XScale: float,
                                YScale: float,
                                ZScale: float,
                                Rotation: float,
                                Overlay: bool,
                                Password: VARIANT = None) -> AcadExternalReference:
        """
        Attaches an external reference (xref) to the drawing.
        
        Like Block objects, attached ExternalReference objects can be nested.
        If another person is editing the drawing to be referenced, the drawing attached is based on the most recently saved version. 
        If the referenced file is missing or corrupt, its data is not displayed in the current drawing. 

        Args:
            PathName (str): The full path and file name of the drawing to be referenced.
            Name (str): The name for the xref to be created.
            InsertionPoint (VARIANT): Variant (three-element array of Doubles)
            XScale (float): The X scaling factor for the xref instance.
            YScale (float): The Y scaling factor for the xref instance.
            ZScale (float): The Z scaling factor for the xref instance.
            Rotation (float): The rotation angle for the xref instance. This angle is specified in radians. 
            Overlay (bool): 
                True: The xref instance is an overlay. 
                False: The xref instance is an attachment. 
            Password (VARIANT, optional): _description_. Defaults to None.

        Returns:
            AcadExternalReference: The newly created ExternalReference object. 
        """
        pass

    def Bind(self, bPrefixName: bool) -> None:
        """
        Binds an external reference (xref) to a drawing.
        
        Binding an xref to a drawing makes the xref a permanent part of the drawing and no longer an externally referenced file. 
        The externally referenced information becomes a block. When the externally referenced drawing is updated, the bound xref is not updated.
        This method binds the entire drawing's database, including all of its dependent symbols. Dependent symbols are named objects such as blocks, 
        dimension styles, layers, linetypes, and text styles. Binding the xref allows named objects from the xref to be used in the current drawing. 

        If the bPrefixName parameter is set to False, the symbol names of the xref drawing are prefixed in the current drawing with <blockname>$x$, 
        where x is an integer that is automatically incremented to avoid overriding existing block definitions. If the bPrefixName parameter is set to True, 
        the symbol names of the xref drawing are merged into the current drawing without the prefix. If duplicate names exist, 
        AutoCAD uses the symbols already defined in the local drawing. If you are unsure whether your drawing contains duplicate symbol names, 
        it is recommended that you set bPrefixName to False. 

        Args:
            bPrefixName (bool): 
                True: Symbol names are not prefixed. 
                False: Symbol names are prefixed with <blockname>$x$.
        """
        pass

    def Detach(self) -> None:
        """
        Detaches an external reference (xref) from a drawing. 
        
        Detaching an xref removes the xref from the current drawing. 
        All copies of the xref are erased, and the xref definition is deleted.
        All xref-dependent symbol table information (such as layers and linetypes) is deleted from the current drawing. 

        You cannot detach an xref that contains other xrefs. 

        """
        pass

    def InsertBlock(self,
                    InsertionPoint: VARIANT,
                    Name: str,
                    Xscale: float,
                    Yscale: float,
                    ZScale: float,
                    Rotation: float,
                    Password: VARIANT = None) -> AcadBlockReference:
        """
        Inserts a drawing file or a named block that has been defined in the current drawing.
        
        Inserting a block into another block will create nested blocks. 

        Attempting to call the InsertBlock method with an uninitialized Name parameter results in unexpected behavior.

        Args:
            InsertionPoint (VARIANT): Variant (three-element array of doubles)
            Name (str): The name of the AutoCAD drawing file or the name of the block to insert. 
                If it is a file name, include the .dwg extension and any path information necessary for AutoCAD to find the file. 
            Xscale (float): _description_. Defaults to 1.
            Yscale (float): _description_. Defaults to 1.
            ZScale (float): _description_. Defaults to 0.
            Rotation (float): _description_. Defaults to 1.
            Password (VARIANT, optional): _description_. Defaults to None.

        Returns:
            AcadBlockReference: The placed block as a Block Reference object. 
        """
        pass

    def Item(self, Index: int) -> IAcadObject:
        """
        Gets the member object at a given index in a collection, group, or selection set.
        
        This method supports string-based iteration. 
        For example, if a block named BLOCK1 was created with the following statement: Set block1 = Blocks.Add("BLOCK1")
        
        you could reference the object through the following statement: Set whichblock = Blocks.Item("BLOCK1")
    
        Args:
            Index (str | int): The index location in the collection for the member item to query. 
            The index must be either an integer or a string. 
            If an integer, the index must be between 0 and N-1, where N is the number of objects in the collection or selection set.

        Returns:
            object: The object at the given index location in the collection or selection set
        """
        pass

    def Reload(self) -> None:
        """
        Reloads the external reference (xref).
        
        When you reload an xref, the most recently saved version of the referenced drawing is loaded into the current drawing. 
        """
        pass

    def Unload(self) -> None:
        """
        Unloads the menu group or external reference.
        
        When an ExternalReference object (xref) is unloaded from the drawing, the drawing opens faster and uses less memory.
        An unloaded xref is not displayed and the xref-dependent symbol table information does not appear in the drawing.
        However, all the information can be restored by reloading the xref using the Reload method. 

        To unload an external reference, you must unload the block that defines the external reference. 
        For example, the following line of VBA code unloads an external reference that is stored in the xrefInserted variable: 
            ThisDrawing.Blocks.Item(xrefInserted.name).Unload
            
        """
        pass

    @property
    def BlockScaling(self) -> acBlockScaling | int:
        """Specifies the scaling allowed for the block."""
        pass

    @BlockScaling.setter
    def BlockScaling(self, val: acBlockScaling | int):
        pass

    @property
    def Comments(self) -> str:
        """Specifies the comments for the block or drawing."""
        pass

    @Comments.setter
    def Comments(self, val: str):
        pass

    @property
    def Count(self) -> int:
        """Gets the number of items in the object."""
        pass

    @property
    def Explodable(self) -> bool:
        """Specifies whether the block can be exploded."""
        pass

    @Explodable.setter
    def Explodable(self, val: bool):
        pass

    @property
    def IsDynamicBlock(self) -> bool:
        """
        Specifies whether this is a dynamic block.
        
        The ComparedReference and ExternalReference objects inherit this property from BlockReference, 
        but this property doesn't affect either of the object types when used. 
        """
        pass

    @property
    def IsLayout(self) -> bool:
        """Determines whether the given block is a layout block. """
        pass

    @property
    def IsXRef(self) -> bool:
        """Determines whether the given block is an XRef block."""
        pass

    @property
    def Layout(self) -> AcadLayout:
        """
        Specifies the layout associated with the model space, paper space, or block object. 
        
        The Layout object contains the plot settings for the model space, paper space, or block object. 

        Named plot settings not associated with a given block are stored as PlotConfiguration objects. 

        Returns:
            AcadLayout: The layout that is associated with the model space, paper space, or block object. 
        """
        pass

    @Layout.setter
    def Layout(self, val: AcadLayout):
        pass

    @property
    def Material(self) -> str:
        """Specifies the name of the material. """
        pass

    @Material.setter
    def Material(self, val: str):
        pass

    @property
    def Name(self) -> str:
        """
        Specifies the name of the object.
        
        A block reference can be assigned the name of only a valid block definition in the drawing. 
        Assigning a block reference a unique name will not automatically create a new block definition. 
        To create a new block definition, use the Add method to add a new Block object to the Blocks collection. 
        """
        pass

    @Name.setter
    def Name(self, val: str):
        pass

    @property
    def Origin(self) -> VARIANT:
        """
        Specifies the origin of the UCS, block, hatch, or raster image in WCS coordinates.

        Returns:
            VARIANT:  Variant (two- or three-element array of doubles)
        """
        pass

    @Origin.setter
    def Origin(self, val: VARIANT):
        pass

    @property
    def Path(self) -> str:
        """Gets the path of the block, document, application, or external reference."""
        pass

    @Path.setter
    def Path(self, val: str):
        pass

    @property
    def Units(self) -> acInsertUnits | int:
        """Specifies the native units of measure for the block."""
        pass

    @Units.setter
    def Units(self, val: acInsertUnits | int):
        pass

    @property
    def XRefDatabase(self) -> AcadDatabase:
        """
        Gets the Database object that defines the contents of the block.
        This property is only available if the IsXRef property for the block equals True.
        """
        pass


class AcadBlocks(IAcadCollection[AcadBlock]):
    pass


class AcadModelSpace(AcadBlock):
    pass


class AcadPaperSpace(AcadBlock):
    pass


class AcadDynamicBlockReferenceProperty(IAcadInterface):
    pass

from __future__ import annotations
from .acadInterface import IAcadInterface
from typing import TYPE_CHECKING, Sequence
from win32com.client import VARIANT

if TYPE_CHECKING:
    from .acadDocuments import AcadDocuments, AcadDocument
    from .acadPreferences import AcadPreferences
    from .acadMenu import AcadMenuGroups, AcadMenuBar


class AcadApplication(IAcadInterface):
    """
    An instance of the AutoCAD application.

    Exemple:
        app = AcadApplication()

        app.Visible = True

        print(app.ActiveDocument.Name)
    """

    def __init__(self, prototype) -> None:
        super().__init__(prototype)

    @property
    def ActiveDocument(self) -> AcadDocument:
        """Specifies the active document (drawing file). """
        pass

    @ActiveDocument.setter
    def ActiveDocument(self, document: AcadDocument):
        pass

    @property
    def Caption(self) -> str:
        """
        Gets the text that the user sees displayed for the application or a menu item.

        Returns:
            Title displayed in the AutoCAD application window or for a menu item on a popup menu.

        """
        pass

    @Caption.setter
    def Caption(self, title: str):
        pass

    @property
    def Documents(self) -> AcadDocuments:
        """Gets the Documents collection. """
        ...

    @property
    def Application(self) -> AcadApplication:
        pass

    @property
    def FullName(self) -> str:
        """
        Gets the name of the application or document, including the path.
        """
        pass

    @property
    def Height(self) -> int:
        pass

    @Height.setter
    def Height(self, height: int):
        pass

    @property
    def HWND(self) -> int:
        """Gets the window handle of the window frame. """
        pass

    @property
    def LocalID(self) -> int:
        """Gets the locale ID of the current AutoCAD session."""
        pass

    @property
    def MenuBar(self) -> AcadMenuBar:
        """Gets the MenuBar object for the session. """
        pass

    @property
    def MenuGroups(self) -> AcadMenuGroups:
        """Gets the MenuGroups collection for the session."""
        pass

    @property
    def Name(self) -> str:
        """Specifies the name of the object. """
        pass

    @property
    def Path(self) -> str:
        """Gets the path of the block, document, application, or external reference. """
        pass

    @property
    def Preferences(self) -> AcadPreferences:
        """Gets the Preferences object. """
        pass

    def StatusID(self, vport) -> bool:
        """Gets the current active status of the viewport. """
        pass

    @property
    def VBE(self):
        """Gets the VBAIDE extensibility object. """
        pass

    @property
    def Version(self) -> str:
        pass

    @property
    def Visible(self) -> bool:
        """Specifies the visibility of an object or the application. """
        pass

    @Visible.setter
    def Visible(self, visible: bool):
        pass

    @property
    def Width(self) -> float:
        """Specifies the width of the object. """
        pass

    @Width.setter
    def Width(self, width: float):
        """Specifies the width of the object. """
        pass

    @property
    def WindowLeft(self) -> int:
        """Specifies the left edge of the application window."""
        pass

    @WindowLeft.setter
    def WindowLeft(self, win_left: int):
        """Specifies the left edge of the application window."""
        pass

    @property
    def WindowTop(self) -> int:
        """Specifies the top edge of the application window."""
        pass

    @WindowTop.setter
    def WindowTop(self, win_top: int):
        """Specifies the top edge of the application window."""
        pass

    @property
    def WindowState(self):
        """
        Specifies the state of the application or document window.

        Returns:
            acWindowState enum
            acMin: The window is minimized.
            acMax: The window is maximized.
            acNorm: The window is normal (neither minimized nor maximized).
        """
        pass

    @WindowState.setter
    def WindowState(self, state):
        pass

    def Eval(self, exp: str):
        """
        Evaluates an expression in VBA.
        """
        pass

    def GetAcadState(self):
        """Gets an AcadState object to monitor the state of AutoCAD from out-of-process applications."""
        pass

    def GetInterfaceObject(self) -> str:
        """Accepts a program ID and attempts to load it into AutoCAD as an in-process server."""
        pass

    def ListARX(self) -> Sequence:
        """Gets the currently loaded ObjectARX applications. """
        pass

    def LoadARX(self, name: str):
        """Loads the specified ObjectARX application. """
        pass

    def LoadDVB(self, name: str):
        """Loads the specified AutoCAD VBA project file. """
        pass

    def Quit(self):
        """Closes the drawing file and exits the AutoCAD application. """
        pass

    def RunMacro(self, path: str):
        """Runs a VBA macro from the Application object. """
        pass

    def UnloadARX(self, name: str):
        pass

    def UnloadDVB(self, name: str):
        pass

    def Update(self):
        """Updates the object to the drawing screen. """
        pass

    def ZoomAll(self):
        """Zooms the current viewport to display the entire drawing."""
        pass

    def ZoomCenter(self, center: VARIANT, maginfy: float):
        """
        Zooms the current viewport to a specified center point and magnification.

        Args:
            center (VARIANT(5 | 8192, x,y,z)): The 3D WCS coordinates specifying the center of the zoom.
            maginfy (float): The magnification level of the window. A value smaller than the current value increases the magnification. A larger value decreases the magnification. 

        """
        pass

    def ZoomExtents(self):
        """Zooms the current viewport to the drawing extents. """
        pass

    def ZoomPickWindow(self):
        """Zooms the current viewport to a window defined by points picked on the screen. """
        pass

    def ZoomPrevious(self):
        """Zooms the current viewport to its previous extents. """
        pass

    def ZoomScaled(self):
        """Zooms the current viewport to given scale factor. """
        pass

    def ZoomWindow(self):
        """Zooms the current viewport to the area specified by two opposite corners of a rectangle. """
        pass

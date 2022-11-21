from dataclasses import dataclass
from enum import Enum, auto


class AcadEnum(Enum):

    def _generate_next_value_(name, start, count, last_values):
        return Enum._generate_next_value_(name, start, count, last_values) - 1


class acLineWeight(AcadEnum):
    # acLnWtByLayer
    # acLnWtByBlock
    acLnWtByLwDefault = -3,
    acLnWt000 = 0,
    acLnWt005 = 5,
    acLnWt009 = 9,
    acLnWt013 = 13,
    acLnWt015 = 15
    acLnWt018 = 18,
    acLnWt020 = 20,
    acLnWt025 = 25,
    acLnWt030 = 30,
    acLnWt035 = 35,
    acLnWt040 = 40,
    acLnWt050 = 50,
    acLnWt053 = 53,
    acLnWt060 = 60,
    acLnWt070 = 70,
    acLnWt080 = 80,
    acLnWt090 = 90,
    acLnWt100 = 100,
    acLnWt106 = 106,
    acLnWt120 = 120,
    acLnWt140 = 140,
    acLnWt158 = 158,
    acLnWt200 = 200,
    acLnWt211 = 211


class acCmColor(AcadEnum):
    pass


class acExtendOption(AcadEnum):
    pass


class acShadePlot(AcadEnum):
    """
    acShadePlotAsDisplayed: Model space view plots the same way it is displayed.
    acShadePlotHidden: Model space view plots with hidden lines removed, regardless of display.
    acShadePlotRendered: Model space view plots as rendered regardless of display.
    acShadePlotWireframe: Model space view plots as wireframe regardless of display.
    """
    pass


class acPlotRotation(AcadEnum):
    ac0degrees = 0
    ac90degrees = 1
    ac180degrees = 2
    ac270degrees = 3


class acPlotPaperUnits(AcadEnum):
    acInches = 0
    acMillimeters = 1
    acPixels = 2


class acPlotType(AcadEnum):
    """
    acDisplay: Prints everything that is in the current display. 
    acExtents: Prints everything that falls within the extents of the currently selected space. 
    acLimits: Prints everything that is in the limits of the current space. 
    acView: Prints the view named by the ViewToPlot property. 
    acWindow: Prints everything in the window specified by the SetWindowToPlot method. 
    acLayout: Prints everything that falls within the margins of the specified paper size with the origin being calculated from 0,0 coordinate location in the Layout tab. This option is not available when printing from model space. 
    """
    pass


class acRegenType(AcadEnum):
    acActiveViewport = 0
    """Regenerates only the active viewport. """
    acAllViewports = 1
    """Regenerates all viewports on the document. """


class acPlotScale(AcadEnum):
    """
    acScaleToFit: Scale to Fit
    ac1_128in_1ft: 1/128"= 1'
    ac1_64in_1ft: 1/64"= 1'
    ac1_32in_1ft: 1/32"= 1'
    ac1_16in_1ft: 1/16"= 1'
    ac3_32in_1ft: 3/32"= 1'
    ac1_8in_1ft: 1/8" = 1'
    ac3_16in_1ft: 3/16"= 1'
    ac1_4in_1ft: 1/4" = 1'
    ac3_8in_1ft: 3/8" = 1'
    ac1_2in_1ft: 1/2" = 1'
    ac3_4in_1ft: 3/4" = 1'
    ac1in_1ft: 1"= 1'
    ac3in_1ft: 3"= 1'
    ac6in_1ft: 6"= 1'
    ac1ft_1ft: 1'= 1'
    ac1_1: 1:1
    ac1_2: 1:2
    ac1_4: 1:4
    ac1_8: 1:8
    ac1_10: 1:10
    ac1_16: 1:16
    ac1_20: 1:20
    ac1_30: 1:30
    ac1_40: 1:40
    ac1_50: 1:50
    ac1_100: 1:100
    ac2_1: 2:1
    ac4_1: 4:1
    ac8_1: 8:1
    ac10_1: 10:1
    ac100_1: 100:1
    """
    pass


class acViewportScale(AcadEnum):
    """
    acVpScaleToFit: Scale to fit
    acVpCustomScale: Custom
    acVp1_128in_1ft: 1/128"= 1'
    acVp1_64in_1ft: 1/64"= 1'
    acVp1_32in_1ft: 1/32"= 1'
    acVp1_16in_1ft: 1/16"= 1'
    acVp3_32in_1ft: 3/32"= 1'
    acVp1_8in_1ft: 1/8" = 1'
    acVp3_16in_1ft: 3/16"= 1'
    acVp1_4in_1ft: 1/4" = 1'
    acVp3_8in_1ft: 3/8" = 1'
    acVp1_2in_1ft: 1/2" = 1'
    acVp3_4in_1ft: 3/4" = 1'
    acVp1and1_2in_1ft: 1-1/2"= 1'
    acVp3in_1ft: 3"= 1'
    acVp6in_1ft: 6"= 1'
    acVp1ft_1ft: 1'= 1'
    acVp1_1: 1:1
    acVp1_2: 1:2
    acVp1_4: 1:4
    acVp1_8: 1:8
    acVp1_10: 1:10
    acVp1_16: 1:16
    acVp1_20: 1:20
    acVp1_30: 1:30
    acVp1_40: 1:40
    acVp1_50: 1:50
    acVp1_100: 1:100
    acVp2_1: 2:1
    acVp4_1: 4:1
    acVp8_1: 8:1
    acVp10_1: 10:1
    acVp100_1: 100:1

    """
    pass


class acHatchObjectType(AcadEnum):
    AcHatchObject = 0
    AcGradientObject = 1


class acPatternType(AcadEnum):
    acHatchPatternTypePredefined = 0
    """Selects the pattern name from those defined in the acad.pat file. """
    acHatchPatternTypeUserDefined = 1
    """Defines a pattern of lines using the current linetype. """
    acHatchPatternTypeCustomDefined = 2
    """Selects the pattern name from a PAT file other than the acad.pat file. """


class acGradientPatternType(AcadEnum):
    acPreDefinedGradient = 0
    """Selects the fill name from one of the standard values. """
    acUserDefinedGradient = 1
    """Defines a pattern based on property values. """


class acLeaderType(AcadEnum):
    acLineNoArrow = 0
    acLineWithArrow = 1
    acSplineNoArrow = 2
    acSplineWithArrow = 3


class acBlockScaling(AcadEnum):
    acAny = 0
    acUniform = 1


class acInsertUnits(AcadEnum):
    """
    acInsertUnitsAngstroms 
acInsertUnitsAstronomicalUnits 
acInsertUnitsCentimeters 
acInsertUnitsDecameters 
acInsertUnitsDecimeters 
acInsertUnitsFeet 
acInsertUnitsGigameters 
acInsertUnitsHectometers 
acInsertUnitsInches 
acInsertUnitsKilometers 
acInsertUnitsLightYears 
acInsertUnitsMeters 
acInsertUnitsMicroinches 
acInsertUnitsMicrons 
acInsertUnitsMiles 
acInsertUnitsMillimeters 
acInsertUnitsMils 
acInsertUnitsNanometers 
acInsertUnitsParsecs 
acInsertUnitsUnitless 
acInsertUnitsUSSurveyFeet 
acInsertUnitsUSSurveyInch 
acInsertUnitsUSSurveyMile 
acInsertUnitsUSSurveyYard 
acInsertUnitsYards"""


class acAlignment(AcadEnum):
    acAlignmentLeft, acAlignmentCenter, acAlignmentRight, acAlignmentAligned, acAlignmentMiddle, \
    acAlignmentFit, acAlignmentTopLeft, acAlignmentTopCenter, acAlignmentTopRight, acAlignmentMiddleLeft, \
    acAlignmentMiddleCenter, acAlignmentMiddleRight, acAlignmentBottomLeft, acAlignmentBottomCenter, acAlignmentBottomRight = range(15)


class acDrawingDirection(AcadEnum):
    acBottomToTop, acByStyle, acLeftToRight, acRightToLeft, acTopToBottom = range(5)


class acTextGenerationFlag(AcadEnum):
    acTextFlagBackward = 0
    acTextFlagUpsideDown = 1


class acSaveAsType(AcadEnum):
    acR12_dxf = auto()
    acR14_dwg = auto()
    ac2000_dwg = auto()
    ac2000_dxf = auto()
    ac2000_Template = auto()
    ac2004_dwg = auto()
    ac2004_dxf = auto()
    ac2004_Template = auto()
    ac2007_dwg = auto()
    ac2007_dxf = auto()
    ac2007_Template = auto()
    ac2010_dwg = auto()
    ac2010_dxf = auto()
    ac2010_Template = auto()
    ac2013_dwg = auto()
    ac2013_dxf = auto()
    ac2013_Template = auto()
    ac2018_dwg = auto()
    ac2018_dxf = auto()
    ac2018_Template = auto()
    acNative = auto()


class AcSelect(AcadEnum):
    acSelectionSetWindow = auto()
    acSelectionSetCrossing = auto()
    acSelectionSetPrevious = auto()
    acSelectionSetLast = auto()
    acSelectionSetAll = auto()

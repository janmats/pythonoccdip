from math import pi

from OCC.Core.gp import gp_Pnt2d, gp_XOY, gp_Lin2d, gp_Ax3, gp_Dir2d
from OCC.Core.AIS import AIS_Shape
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Core.Geom import Geom_CylindricalSurface
from OCC.Core.GCE2d import GCE2d_MakeSegment
from pythonocclab.lab_web import buildWrench, buildBrick

from OCC.Display.SimpleGui import init_display

display, start_display, add_menu, add_function_to_menu = init_display()


figure = buildBrick()


display.DisplayShape(figure)

start_display()

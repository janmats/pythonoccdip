from math import pi

from OCC.Core.gp import gp_Pnt2d, gp_XOY, gp_Lin2d, gp_Ax3, gp_Dir2d
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Core.Geom import Geom_CylindricalSurface
from OCC.Core.GCE2d import GCE2d_MakeSegment

from OCC.Display.WebGl import threejs_renderer
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse, BRepAlgoAPI_Common
from OCC.Core.BRepFilletAPI import BRepFilletAPI_MakeFillet, BRepFilletAPI_MakeChamfer
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCC.Core.Graphic3d import Graphic3d_NameOfMaterial, Graphic3d_NOM_COPPER, Graphic3d_MaterialAspect
from OCC.Core.gp import gp_Pnt, gp_Ax2, gp_Dir
from OCC.Core.AIS import AIS_Shape, AIS_Shaded
from OCC.Core.GC import GC_MakeArcOfCircle, GC_MakeSegment


from OCC.Display.SimpleGui import init_display
from OCC.Extend.TopologyUtils import TopologyExplorer

Boxmain = BRepPrimAPI_MakeBox(60.0, 60.0, 10.0).Shape()



#скругление Boxmain
rake1 = BRepFilletAPI_MakeFillet(Boxmain)
expl = list(TopologyExplorer(Boxmain).edges())
rake1.Add(8, 8, expl[0])
rake1.Add(8, 8, expl[4])
rake1.Build()
evolved_Boxmain = rake1.Shape()

axe1 = gp_Ax2(gp_Pnt(8, 8, 0), gp_Dir(0, 0, 1))
cylinder1 = BRepPrimAPI_MakeCylinder(axe1, 4, 10).Shape()
axe2 = gp_Ax2(gp_Pnt(52, 8, 0), gp_Dir(0, 0, 1))
cylinder2 = BRepPrimAPI_MakeCylinder(axe2, 4, 10).Shape()
cut1 = BRepAlgoAPI_Cut(evolved_Boxmain, cylinder1).Shape()
cut2 = BRepAlgoAPI_Cut(cut1, cylinder2).Shape()

axe3 = gp_Ax2(gp_Pnt(0, 50, 0), gp_Dir(0, 0, 1))
box2 = BRepPrimAPI_MakeBox(axe3, 60.0, 10.0, 60.0).Shape()


chamfer1 = BRepFilletAPI_MakeChamfer(box2)
expl = list(TopologyExplorer(box2).edges())
box1faces = list(TopologyExplorer(box2).faces())
chamfer1.Add(50.0, 15.0, expl[1], box1faces[0])
chamfer1.Add(50.0, 15.0, expl[5], box1faces[0])
chamfer1.Build()
evolved_box1 = chamfer1.Shape()

fuse1 = BRepAlgoAPI_Fuse(evolved_box1, cut2).Shape()

axe4 = gp_Ax2(gp_Pnt(30, 60, 60), gp_Dir(0, -1, 0))
axe5 = gp_Ax2(gp_Pnt(30, 50, 60), gp_Dir(0, -1, 0))
cylinder4 = BRepPrimAPI_MakeCylinder(axe5, 7.5, 30).Shape()
cylinder3 = BRepPrimAPI_MakeCylinder(axe4, 15, 40).Shape()
cut3 = BRepAlgoAPI_Cut(cylinder3, cylinder4).Shape()
axe6 = gp_Ax2(gp_Pnt(30, 40, 65), gp_Dir(0, 0, 1))
cylinder5 = BRepPrimAPI_MakeCylinder(axe6, 4, 20).Shape()
cut4 = BRepAlgoAPI_Cut(cut3, cylinder5).Shape()
fuse2 = BRepAlgoAPI_Fuse(fuse1, cut4).Shape()

axe7 = gp_Ax2(gp_Pnt(25, 60, 47.5), gp_Dir(0, -1, 0))
box3 = BRepPrimAPI_MakeBox(axe7, 40.0, 10.0, 50.0).Shape()
chamfer2 = BRepFilletAPI_MakeChamfer(box3)
expl = list(TopologyExplorer(box3).edges())
box1faces = list(TopologyExplorer(box3).faces())
chamfer2.Add(10.5, 37.5, expl[1], box1faces[0])
chamfer2.Build()
evolved_box3 = chamfer2.Shape()
cut5 = BRepAlgoAPI_Cut(evolved_box3, cylinder3).Shape()
fuse3 = BRepAlgoAPI_Fuse(fuse2, cut5).Shape()
axe8 = gp_Ax2(gp_Pnt(-0.1, 50, 0), gp_Dir(0, 1, 0))
fuse4 = BRepPrimAPI_MakeBox(axe8, 10.0, 0.01, 10.0).Shape()
axe9 = gp_Ax2(gp_Pnt(60.1, 50, 0), gp_Dir(0, 1, 0))
fuse5 = BRepPrimAPI_MakeBox(axe9, 10.0, 0.01, 10.0).Shape()

rake2 = BRepFilletAPI_MakeFillet(fuse3)
expl = list(TopologyExplorer(fuse3).edges())
print(len(expl))
rake2.Add(1, 1, expl[37])
rake2.Add(1, 1, expl[38])
rake2.Add(1, 1, expl[41])
rake2.Add(1, 1, expl[59])
rake2.Add(1, 1, expl[23])
rake2.Add(1, 1, expl[22])
rake2.Add(1, 1, expl[21])
rake2.Add(1, 1, expl[20])
rake2.Add(1, 1, expl[19])
rake2.Build()
evolved_Figura = rake2.Shape()

fuse6 = BRepAlgoAPI_Fuse(evolved_Figura, fuse4).Shape()
fuse7 = BRepAlgoAPI_Fuse(fuse6, fuse5).Shape()

display = threejs_renderer.ThreejsRenderer()
display.DisplayShape(fuse7, color=(1, 0, 0), line_width=1.0)
display.render()
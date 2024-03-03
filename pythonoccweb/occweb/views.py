import os.path
import sys

from django.views.decorators.clickjacking import xframe_options_exempt

sys.path.append('../')

from django.shortcuts import render
from django.conf import settings
from OCC.Display.WebGl import x3dom_renderer
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeSphere
from pythonocclab.lab_web import buildPart
from django.http import HttpResponse
from pythonocclab import custom_x3dom_renderer


# Create your views here.
class CustomX3DomRenderer(custom_x3dom_renderer.X3DomRenderer):
    def render_to_string(self):
        # N.B. Writing the html file to disk isn't really needed; you
        # could also build the string directly without writing it
        # to disk
        self.generate_html_file(self._axes_plane, self._axes_plane_zoom_factor)
        return open(self._html_filename, 'r').read()

def index(request):
    return render(request, 'index.html')


def showPart(request):
    shape = buildPart()
    my_renderer = CustomX3DomRenderer(path=os.path.join('static/'))
    my_renderer.DisplayShape(shape)
#    return HttpResponse(my_renderer.render_to_string())
    return render(request, "showShape.html")


def showBox(request):
    shape = BRepPrimAPI_MakeBox(10, 10, 10).Shape()
    my_renderer = CustomX3DomRenderer(path=os.path.join('static/'))
    my_renderer.DisplayShape(shape)
#    return HttpResponse(my_renderer.render_to_string())
    return render(request, "showShape.html")

def showSphere(request):
    shape = BRepPrimAPI_MakeSphere(5).Shape()
    my_renderer = CustomX3DomRenderer(path=os.path.join('static/'))
    my_renderer.DisplayShape(shape)
#    return HttpResponse(my_renderer.render_to_string())
    return render(request, "showShape.html")

def help(request):
    return render(request, 'help.html')

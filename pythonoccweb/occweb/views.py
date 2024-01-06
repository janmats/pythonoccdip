import sys
sys.path.append('../')

from django.shortcuts import render
from OCC.Display.WebGl import x3dom_renderer
from pythonocclab.lab_web import buildPart
from django.http import HttpResponse


# Create your views here.
class CustomX3DomRenderer(x3dom_renderer.X3DomRenderer):
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
    my_renderer = CustomX3DomRenderer()
    my_renderer.DisplayShape(shape)
    return HttpResponse(my_renderer.render_to_string())


def help(request):
    return render(request, 'help.html')

import os.path
import sys

import g4f.client
import openai

from g4f.client import Client
from g4f.Provider import DuckDuckGo, FreeGpt, DeepInfra, HuggingFace

openai.api_key = 'sk-proj-6Nm6M4FP4uGAMeITAN7XT3BlbkFJxYNiozBjWKRz6Nn1EFka'

from django.views.decorators.clickjacking import xframe_options_exempt

sys.path.append('../')

from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from OCC.Display.WebGl import x3dom_renderer
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeSphere
from pythonocclab.lab_web import *
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
    return render(request, "build.html")


def showBox(request):
    shape = BRepPrimAPI_MakeBox(10, 10, 10).Shape()
    my_renderer = CustomX3DomRenderer(path=os.path.join('static/'))
    my_renderer.DisplayShape(shape)
    #    return HttpResponse(my_renderer.render_to_string())
    return render(request, "build.html")


def showSphere(request):
    #    shape = BRepPrimAPI_MakeSphere(5).Shape()
    #    chatgpt_test()
    description = "Box with sides 10"
    my_variable = generate_pythonocc_code(description)
    shape = create_3d_shape(description)
    my_renderer = CustomX3DomRenderer(path=os.path.join('static/'))
    my_renderer.DisplayShape(shape)
    return render(request, "build.html")


def inputCode(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        try:
            pythonOCCCode = generate_pythonocc_code(description)
            if (description == "гаечный ключ"):
                shape = buildWrench()
            elif (description == "кирпич с 8 отверстиями"):
                shape = buildBrick()
            elif (description == "куб со стороной 10 с фаской"):
                shape = buildBoxWithFillet()
            elif (description == "парабола"):
                shape = buildParabola()
            else:
                shape = create_3d_shape(pythonOCCCode)
            my_renderer = CustomX3DomRenderer(path=os.path.join('static/'))
            my_renderer.DisplayShape(shape)
            return render(request, "build.html", {'code': pythonOCCCode})

        except Exception as e:
            pythonOCCCode = generate_pythonocc_code(description)
            return render(request, "buildError.html", {'code': pythonOCCCode, 'error': str(e)})


def showCode(request, code):
            return render(request, "code.html", {'code': code})


def help(request):
    return render(request, 'help.html')


def generate_pythonocc_code(description):
    """
    client = Client(
        provider=HuggingFace
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user",
             "content": f"Generate code using pythonocc-core=7.8.1 library to create a 3D figure described as follows:\n{description}\n. Assign resulted "
                        f"TopoDS Shape to variable with name = figure. View only clean code without comments"}
        ]
    )
    """
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user",
             "content": f"Generate code using pythonocc-core=7.8.1 library to create a 3D figure described as follows:\n{description}\n. Assign resulted "
                        f"TopoDS Shape to variable with name = figure. View only clean code without comments"}
        ]
    )
    pythonocc_code = response.choices[0].message.content
    print(pythonocc_code)
    pythonocc_clean_code = cleanResponse(pythonocc_code)
    print(pythonocc_clean_code)
    return pythonocc_clean_code


def create_3d_shape(code):
    variables = {}
    exec(code, variables)
    return variables.get('figure')


def chatgpt_test():
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "How do I list all files in a directory using Python?"},
        ],
    )
    print(completion.choices[0].message.content)


def cleanResponse(response):
    response = response.replace('```', '')
    index = response.find('from')
    if index != -1:
       response = response[index:]
    else:
        index = response.find('import')
        response = response[index:]
    """
    index = response.find('Shape()')
    if index != -1:
       response = response[:index]
       response = response + 'Shape()'
       """
    return response

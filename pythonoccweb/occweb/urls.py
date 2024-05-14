from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("help", views.help, name="help"),
    path("showPart", views.showPart, name="showPart"),
    path("showBox", views.showBox, name="showBox"),
    path("showSphere", views.showSphere, name="showSphere"),
    path('showShape', TemplateView.as_view(template_name="showShape.html"), name='showShape'),
    path('inputCode/', views.inputCode, name='inputCode'),
    path('showCode/<str:code>', views.showCode, name='showCode'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_form),
    # path('', views.getData)
]

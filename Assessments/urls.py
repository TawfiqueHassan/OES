from django.urls import path 
from . import views
app_name = 'Assessments'
urlpatterns = [
    path('', views.index , name="index"),
    path('attempt/<id>/',views.attempt,name='attempt'),
    path('attempt/<id>/result/<marks>/',views.result,name='result'),
    
]
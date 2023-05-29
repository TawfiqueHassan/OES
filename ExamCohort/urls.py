from django.urls import path 
from . import views

app_name = 'ExamCohort'
urlpatterns = [
    path('',views.index,name='index'),
    path('createcohort/', views.createcohort , name="createcohort" ),
    path('createassessment/',views.createassessment,name="createassessment"),
    path('addcandidates/',views.addcandidates,name="addcandidates"),
    path('createquestion/<id>/',views.createquestion,name='createquestion'),
    path('createmcq/<id>/',views.createmcq,name="createmcq"),
    path('createmicroviva/<id>/',views.createmicroviva,name="createmicroviva"),
]
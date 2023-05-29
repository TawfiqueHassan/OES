from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ExamCohort.models import ExamCohort
# Create your views here.

def index(request):
    return render(request, "login/index.html")
@login_required(login_url='/')
def homepage(request):
    if(ExamCohort.objects.filter(pk=request.user.id).exists()):
        query_set=ExamCohort.objects.filter(pk=request.user.id)
        return render(request, "homepage/homepage.html", {'name':query_set[0]})  
    else:
        return render(request, "homepage/HomepageCreate.html")
        
    
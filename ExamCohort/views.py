from fileinput import filename
import imp
from multiprocessing import context
from pickle import GET
from tkinter import TRUE
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from .forms import ExamCohortForm,createassessmentform,createmcqform,addcandidatesform
from ExamCohort.models import ExamCohort,Assessments,Questions,MicroViva,Candidates,User
import datetime
from django.forms import ValidationError
from django.contrib import messages
import uuid
import speech_recognition as sr
import ffmpeg,subprocess
import tempfile
# Create your views here.
@login_required(login_url='/')
def createcohort(request):
    if request.method == 'POST':
        form = ExamCohortForm(request.POST)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.EvaluatorId = request.user
            temp.save()
            return HttpResponseRedirect('/homepage')
    else:
        form = ExamCohortForm()
    return render(request, 'createcohort.html', {'form': form})
@login_required(login_url='/')
def index(request):
    if(Assessments.objects.filter(EvaluatorId_id=request.user.id).exists()):
        query_set=Assessments.objects.filter(EvaluatorId_id=request.user.id)
        context = {
        "object_list": query_set,
        "name": query_set[0]
        }
        return render(request, "index.html",context)
    else:
        return render(request, "index.html")

@login_required(login_url='/')
def addcandidates(request):
    query_set=User.objects.exclude(id=request.user.id).exclude(is_staff=1)
    if request.method == 'POST':
        form = addcandidatesform(request.POST)
        if form.is_valid():
            temp = form.save(commit=False)
            if(Candidates.objects.filter(user_email=temp.user_email,EvaluatorId=request.user.id)):
                messages.error(request, 'User Already Added')
                form = addcandidatesform()
                return render(request, 'addcandidates.html', {'form': form,'object_list':query_set})
            elif(temp.user_email==request.user.email):
                messages.error(request, 'Evaluator cannot be a candidate')
                form = addcandidatesform()
                return render(request, 'addcandidates.html', {'form': form,'object_list':query_set})


            if(User.objects.filter(email=temp.user_email).exists()):
                temp.user=User.objects.get(email=temp.user_email)
                temp.EvaluatorId = ExamCohort.objects.get(EvaluatorId=request.user.id)
                temp.save()
                messages.error(request, 'Added candidate')
            else:
                messages.error(request, 'Email Does Not Exist')
                form = addcandidatesform()
                return render(request, 'addcandidates.html', {'form': form,'object_list':query_set})
    else:
        form = addcandidatesform()
    return render(request, 'addcandidates.html', {'form': form,'object_list':query_set})


    

@login_required(login_url='/')
def createassessment(request):
    if request.method == 'POST':
        form = createassessmentform(request.POST)
        if form.is_valid():
            temp= form.save(commit=False)
            temp.EvaluatorId = ExamCohort.objects.get(pk=request.user)
            now = datetime.datetime.now()
            currenttimestamp = now.timestamp()
            startDatestamp = temp.startDate.timestamp()
            dueDatestamp=temp.dueDate.timestamp()
            if startDatestamp < currenttimestamp :
                form = createassessmentform()
                messages.error(request, 'Start Date Time cannot be before Current Date time')
                return render(request, 'createassessment.html', {'form': form})
            elif dueDatestamp < startDatestamp :
                form = createassessmentform()
                messages.error(request, 'Due Date Time cannot be before Start Date time')
                return render(request, 'createassessment.html', {'form': form})
            temp.save()
            return HttpResponseRedirect('/ExamCohort')
    else:
        print("Invalid")
        form = createassessmentform()
    return render(request, 'createassessment.html', {'form': form})

@login_required(login_url='/')
def createquestion(request,id):
    query_set=Questions.objects.all().select_related('mcq','microviva').filter(Assessment=id)

    #command='ffmpeg -i '+r'C:\Users\tawfi\OneDrive\Desktop\CSE327\summer2022.cse327.2.10\OES\media\records\audio_7c99300f-2.webm'+' -vn -y '+r'C:\Users\tawfi\OneDrive\Desktop\CSE327\summer2022.cse327.2.10\OES\media\records\out1.wav'
    #subprocess.run(command,shell=True)

#    r=sr.Recognizer()
#    with sr.AudioFile(r"C:\Users\tawfi\OneDrive\Desktop\CSE327\summer2022.cse327.2.10\OES\media\records\out1.wav") as source:
#        audio=r.listen(source)
#    text=r.recognize_google(audio)
#    print(text)



    context = {
    "Assessment_ID": id,
    "query_set":query_set,
    }
    return render(request, 'createquestion.html',context )

def createmcq(request,id):
    if request.method == 'POST':
        form = createmcqform(request.POST)
        if form.is_valid():
            temp= form.save(commit=False)
            temp.Assessment = Assessments.objects.get(pk=id)
            flag=False
            if(temp.Answer==temp.Choice_1):
                flag=True
            elif(temp.Answer==temp.Choice_2):
                flag=True
            elif(temp.Answer==temp.Choice_3):
                flag=True
            elif(temp.Answer==temp.Choice_4):
                flag=True
            elif(temp.Answer==""):
                flag=False
                messages.error(request, 'Answer cannot be empty')
            if(flag):
                temp.save()
            else:
                messages.error(request, 'Answer is not from the choices')
                form = createmcqform()
                return render(request, 'createmcq.html', {'form': form})            
            return HttpResponseRedirect('/ExamCohort/createquestion/%s' %id)
    else:
        form = createmcqform()
    return render(request, 'createmcq.html', {'form': form})    

def createmicroviva(request,id):
    audio_file_name = str(uuid.uuid1())
    answer_file_name="answer_"+audio_file_name
    context = {"file_name": "audio_"+audio_file_name[0:10],
                "answer_file_name":answer_file_name[0:10]
    }
    if request.method == 'POST':
        temp = Assessments.objects.get(pk=id)
        audio_file = request.FILES.get('recorded_audio')
        audio_file2= request.FILES.get('recorded_audio2')

        myObj = MicroViva(Question_name=audio_file_name, voice_record=audio_file,Assessment=temp,Answer_name=answer_file_name,answer_record=audio_file2)
        myObj.save()
        
        command='ffmpeg -i '+r'C:\Users\tawfi\Desktop\CSE327\summer2022.cse327.2.10\OES\media\%s'%myObj.answer_record+' -vn -y '+r'C:\Users\tawfi\Desktop\CSE327\summer2022.cse327.2.10\OES\media\records\answer_text.wav'
        subprocess.run(command,shell=True)
        r=sr.Recognizer()
        with sr.AudioFile(r"C:\Users\tawfi\Desktop\CSE327\summer2022.cse327.2.10\OES\media\records\answer_text.wav") as source:
            audio=r.listen(source)
        text=r.recognize_google(audio)
        print(text)
        myObj.Answer_text=text
        myObj.save()

        return HttpResponseRedirect('/ExamCohort/createquestion/%s'%id)
    return render(request, 'createmicroviva.html',context)  
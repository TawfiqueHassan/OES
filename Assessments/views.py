from multiprocessing import context
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from ExamCohort.models import Candidates,Assessments,Questions
from Assessments.models import Marksheet
from django.db.models import Q
import datetime
import random
import uuid
from difflib import SequenceMatcher
import ffmpeg,subprocess
import speech_recognition as sr
# Create your views here.
@login_required(login_url='/')
def index(request):
    ids=Candidates.objects.filter(user=request.user).values_list('EvaluatorId', flat=True)
    query_set=Assessments.objects.filter(EvaluatorId__in=ids).exclude(dueDate__lt=datetime.datetime.now())
    context = {
        "object_list": query_set,
        }
    return render(request, "Assessments.html",context)

def attempt(request,id):
    if request.method == 'GET':
        if(Marksheet.objects.filter(Q(Candidate_Id=request.user)&Q(Assessment_Name=id)).exists()):
            query_set=Questions.objects.all().select_related('mcq','microviva').filter(Assessment=id)
            while(1):
                send=random.choice(list(query_set))
                check=Marksheet.objects.get(Question=send)
                if(check.Attempted=='no'): 
                    try:
                        if(send.mcq):
                            ls=[]
                            ls.append(send.mcq.Choice_1)
                            ls.append(send.mcq.Choice_2)
                            ls.append(send.mcq.Choice_3)
                            ls.append(send.mcq.Choice_4)
                            random.shuffle(ls)
                            send.mcq.Choice_1=ls[0]
                            send.mcq.Choice_2=ls[1]
                            send.mcq.Choice_3=ls[2]
                            send.mcq.Choice_4=ls[3]
                            context = {
                            "object_list": send,
                            "Assessment_ID":id,
                        }
                        return render(request, "attempt.html",context)
                    except:
                            audio_file_name = str(uuid.uuid1())
                            context = {
                            "file_name": "Attempt_Answer"+audio_file_name[0:10],
                            "object_list": send,
                            "Assessment_ID":id,
                            }
                            return render(request, "attempt.html",context)
                elif(Marksheet.objects.filter(Q(Candidate_Id=request.user)&Q(Attempted='no')& Q(Assessment_Name=id)).exists()):
                    continue
                else:
                    query_set=Marksheet.objects.filter(Q(Candidate_Id=request.user) & Q(Assessment_Name=id))
                    value=0
                    marks=0
                    for i in query_set:
                        marks=marks+i.Mark
                        value=value+1
                    return HttpResponseRedirect('result/%s'%marks)
        else:
            query_set=Questions.objects.all().select_related('mcq','microviva').filter(Assessment=id)
            for i in query_set:
                obj=Marksheet()
                obj.Candidate_Id=request.user
                obj.Assessment_Name=Assessments.objects.get(pk=id)
                obj.Question=i
                obj.Right_Answer='Answer'
                obj.Given_Answer=''
                obj.Attempted='no'
                obj.Mark=0
                obj.save()
            
            return attempt(request,id)
    elif request.method == 'POST':
        if 'skip' in request.POST:
            Question_obj=Questions.objects.get(Assessment=id,id=request.POST['id'])
            if(Question_obj.mcq):
                Edit_obj=Marksheet.objects.get(Candidate_Id=request.user,Assessment_Name=id,Question=request.POST['id'])
                Edit_obj.Attempted='skip'
                Edit_obj.Given_Answer='skipped'
                Edit_obj.Right_Answer=Question_obj.mcq.Answer
                Edit_obj.save()
            else:
                pass
        else:
            Question_obj=Questions.objects.get(Assessment=id,id=request.POST['id'])
            try:
                if(Question_obj.mcq):
                    Edit_obj=Marksheet.objects.get(Candidate_Id=request.user,Assessment_Name=id,Question=request.POST['id'])
                    Edit_obj.Attempted='yes'
                    Edit_obj.Given_Answer=request.POST['answer']
                    Edit_obj.Right_Answer=Question_obj.mcq.Answer
                    if(Edit_obj.Given_Answer==Edit_obj.Right_Answer):
                        Edit_obj.Mark=Question_obj.mcq.Mark
                    else:
                        Edit_obj.Mark=0
                    Edit_obj.save()
            except:
                Edit_obj=Marksheet.objects.get(Candidate_Id=request.user,Assessment_Name=id,Question=request.POST['id'])
                audio_file = request.FILES.get('recorded_audio')
                Edit_obj.Right_Answer=Question_obj.microviva.Answer_text
                Edit_obj.Viva_answer=audio_file
                Edit_obj.Attempted='yes'
                Edit_obj.save()

                command='ffmpeg -i '+r'C:\Users\tawfi\Desktop\CSE327\summer2022.cse327.2.10\OES\media\%s'%Edit_obj.Viva_answer+' -vn -y '+r'C:\Users\tawfi\Desktop\CSE327\summer2022.cse327.2.10\OES\media\records\Viva_answer_text.wav'
                subprocess.run(command,shell=True)
                r=sr.Recognizer()
                with sr.AudioFile(r"C:\Users\tawfi\Desktop\CSE327\summer2022.cse327.2.10\OES\media\records\Viva_answer_text.wav") as source:
                    audio=r.listen(source)
                text=r.recognize_google(audio)
                print(text)
                Edit_obj.Given_Answer=text
                Rans=Edit_obj.Right_Answer.lower().split()
                Gans=Edit_obj.Given_Answer.lower().split()
                flag=0
                for word in Gans:
                    if word in Rans:
                        flag=flag+1

                if(flag==len(Rans)):
                    Edit_obj.Mark=1

                Edit_obj.save()
                


        query_set=Questions.objects.all().select_related('mcq','microviva').filter(Assessment=id)
        while(1):
            send=random.choice(list(query_set))
            check=Marksheet.objects.get(Question=send)
            if(check.Attempted=='no'):
                try:
                    if(send.mcq):
                        ls=[]
                        ls.append(send.mcq.Choice_1)
                        ls.append(send.mcq.Choice_2)
                        ls.append(send.mcq.Choice_3)
                        ls.append(send.mcq.Choice_4)
                        random.shuffle(ls)
                        send.mcq.Choice_1=ls[0]
                        send.mcq.Choice_2=ls[1]
                        send.mcq.Choice_3=ls[2]
                        send.mcq.Choice_4=ls[3]
                        context = {
                        "object_list": send,
                        "Assessment_ID":id,
                        }
                        return render(request, "attempt.html",context)
                except:
                        audio_file_name = str(uuid.uuid1())
                        context = {
                        "file_name": "Attempt_Answer"+audio_file_name[0:10],
                        "object_list": send,
                        "Assessment_ID":id,
                        }
                        return render(request, "attempt.html",context)
            elif(Marksheet.objects.filter(Q(Candidate_Id=request.user) & Q(Attempted='no')& Q(Assessment_Name=id)).exists()):
                continue
            else:
                query_set=Marksheet.objects.filter(Q(Candidate_Id=request.user) & Q(Assessment_Name=id))
                value=0
                marks=0
                for i in query_set:
                    marks=marks+i.Mark
                    value=value+1
                return HttpResponseRedirect('result/%s'%marks)




def result(request,marks,id):
    context={
        'marks': marks,
    }
    return render(request, "result.html",context)


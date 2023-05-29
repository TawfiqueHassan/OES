from tkinter import CASCADE
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class ExamCohort(models.Model):
    EvaluatorId= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    name =models.CharField(max_length=15)

    def __str__(self) -> str:
        return self.name

class Assessments(models.Model):
    EvaluatorId=models.ForeignKey(ExamCohort, on_delete=models.CASCADE)
    name=models.CharField(max_length=15)
    startDate=models.DateTimeField()
    dueDate=models.DateTimeField()

    def __str__(self) -> str:
        return self.name


class Candidates(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_email=models.EmailField()
    EvaluatorId =models.ForeignKey(ExamCohort, on_delete=models.CASCADE)



class Questions(models.Model):
    Assessment=models.ForeignKey(Assessments, on_delete=models.CASCADE)

    
    
class MCQ(Questions):
    Question_Text= models.CharField(max_length=255)
    Choice_1 = models.CharField(max_length=50)
    Choice_2 = models.CharField(max_length=50)
    Choice_3 = models.CharField(max_length=50)
    Choice_4= models.CharField(max_length=50)
    Answer=models.CharField(max_length=50)
    Mark=models.IntegerField()
    Time_limit_in_seconds=models.IntegerField(
        default=30,
        validators=[
            MaxValueValidator(300),
            MinValueValidator(10)
        ]
     )
    def __str__(self) -> str:
        return self.Question_Text

class MicroViva(Questions):  
    Question_name = models.CharField(null=True, blank=True, max_length=200)
    voice_record = models.FileField(null=True, blank=True, upload_to="records")
    Answer_name= models.CharField(null=True, blank=True, max_length=200)
    answer_record= models.FileField(null=True, blank=True, upload_to="records")
    Answer_text=models.CharField(max_length=50)

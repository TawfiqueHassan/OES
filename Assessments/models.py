from django.db import models
from django.contrib.auth.models import User
from ExamCohort.models import Assessments,Questions
# Create your models here.
class Marksheet(models.Model):  
    Candidate_Id = models.ForeignKey(User, on_delete=models.CASCADE)
    Assessment_Name=models.ForeignKey(Assessments, on_delete=models.CASCADE)
    Question=models.ForeignKey(Questions, on_delete=models.CASCADE)
    Right_Answer=models.CharField(max_length=100)
    Given_Answer=models.CharField(max_length=100)
    Attempted= models.CharField(max_length=50)
    Mark=models.IntegerField()
    Viva_answer = models.FileField(null=True, blank=True, upload_to="records")

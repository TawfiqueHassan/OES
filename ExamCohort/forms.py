from dataclasses import field
from django import forms
from .models import ExamCohort,Assessments,MCQ,Candidates
from bootstrap_datepicker_plus.widgets import DateTimePickerInput


class ExamCohortForm(forms.ModelForm):
        class Meta:         
            model = ExamCohort       
            fields = ['name']
            widgets = {
                'name': forms.TextInput(attrs={'class':'form-control'}),
            }

class createassessmentform(forms.ModelForm):
    class Meta:
       model = Assessments
       fields=['name','startDate','dueDate']
       widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'startDate' : DateTimePickerInput(),
            'dueDate':DateTimePickerInput(),

       }


class addcandidatesform(forms.ModelForm):
    class Meta:
       model = Candidates
       fields=['user_email']
       widgets = {
            'user_email': forms.EmailInput(attrs={'class':'form-control'}),

       }

class createmcqform(forms.ModelForm):
    class Meta:
       model = MCQ
       fields=['Question_Text','Choice_1','Choice_2','Choice_3','Choice_4','Answer','Mark','Time_limit_in_seconds']
       widgets = {
            'Question_Text': forms.TextInput(attrs={'class':'form-control'}),
            'Choice_1': forms.TextInput(attrs={'class':'form-control'}),
            'Choice_2': forms.TextInput(attrs={'class':'form-control'}),
            'Choice_3': forms.TextInput(attrs={'class':'form-control'}),
            'Choice_4': forms.TextInput(attrs={'class':'form-control'}),
            'Answer': forms.TextInput(attrs={'class':'form-control'}),
            'Mark': forms.TextInput(attrs={'class':'form-control'}),
            'Time_limit_in_seconds': forms.TextInput(attrs={'class':'form-control'}),
       }


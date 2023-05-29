from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.ExamCohort)
admin.site.register(models.Assessments)
admin.site.register(models.Questions)
admin.site.register(models.MCQ)
admin.site.register(models.MicroViva)
admin.site.register(models.Candidates)



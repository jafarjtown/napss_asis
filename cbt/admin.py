from django.contrib import admin
from .models import CourseCBT, Option, Question , TrueFalseQuestion, EssayQuestion, FillInTheBlanksQuestion
# Register your models here.
admin.site.register(CourseCBT)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(TrueFalseQuestion)
admin.site.register(FillInTheBlanksQuestion)
admin.site.register(EssayQuestion)
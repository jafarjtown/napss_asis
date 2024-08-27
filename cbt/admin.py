from django.contrib import admin
from .models import CourseCBT, Option, Question , TrueFalseQuestion, EssayQuestion, FillInTheBlanksQuestion
# Register your models here.
class OptionInline(admin.TabularInline):
    model = Option
    extra = 4


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['course', 'question']
    list_filter = ['course']
    search_fields = ['question']
    inlines = [OptionInline]


admin.site.register(Question, QuestionAdmin)

admin.site.register(CourseCBT)
#admin.site.register(Question)
#-admin.site.register(Option)
admin.site.register(TrueFalseQuestion)
admin.site.register(FillInTheBlanksQuestion)
admin.site.register(EssayQuestion)
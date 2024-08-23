from django.forms import ModelForm, CharField, RadioSelect
from django import forms
from .models import Question, Option, TrueFalseQuestion

class OptionForm(ModelForm):
    #value = CharField(required=False)
    class Meta:
        model = Option
        fields = "__all__"
        


class QuestionForm(ModelForm):
    class Meta:
        model = Question 
        fields = ["question"]


class TrueFalseQuestionForm(ModelForm):
    class Meta:
        model = TrueFalseQuestion
        fields = ['question_text', 'correct_answer']
        widgets = {
            'question_text': forms.Textarea(attrs={'rows': 4, 'cols': 40})
        }

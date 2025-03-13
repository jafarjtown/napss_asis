from django.db import models
from django.db.models import QuerySet

def randomize_options(qs: QuerySet) -> QuerySet:
    from random import shuffle
    list_of_options = list(qs) 
    shuffle(list_of_options)
    return list_of_options
# Create your models here.
class CourseCBT(models.Model):
  course = models.OneToOneField('material.Course', on_delete=models.CASCADE, related_name='cbt_test')
  objectives = models.ManyToManyField('Question', blank=True)
  essays = models.ManyToManyField('EssayQuestion', blank=True)
  fill_the_blank = models.ManyToManyField('FillInTheBlanksQuestion', blank=True)
  true_false = models.ManyToManyField('TrueFalseQuestion', blank=True)
  

class Question(models.Model):
    course = models.ForeignKey('material.Course', on_delete=models.CASCADE, null=True, related_name='objectives')
    question = models.TextField()
    
    @property
    def correct_answer(self):
        for o in self.opts.all():
            if o.is_correct:
                return o
    @property
    def options(self):
        options = self.opts.all()  # Get all options for the question
        return randomize_options(options) 
    
    @property
    def a(self):
      return self.opts.first()
      
    @property
    def b(self):
      return self.opts.all()[1]
        
    @property
    def c(self):
      return self.opts.all()[2]
        
    @property
    def d(self):
      return self.opts.last()
        
class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, related_name='opts')
    value = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    

class EssayQuestion(models.Model):
    question = models.TextField()

class FillInTheBlanksQuestion(models.Model):
    blanks = models.TextField(help_text="Enter blanks separated by [BLANK]. Example: The capital of [BLANK] is [BLANK].")
    correct_answers = models.TextField(help_text="Enter correct answers separated by commas. Example: Paris, France")
    
    def get_blanks_list(self):
        return self.blanks.split("[BLANK]")

    def get_correct_answers_list(self):
        return [answer.strip() for answer in self.correct_answers.split(",")]

    def is_answer_correct(self, user_answers):
        correct_answers = self.get_correct_answers_list()
        return user_answers == correct_answers

    def __str__(self):
        return self.blanks
    
    def parse_html(self):
        return self.blanks.replace('[BLANK]', '<input type="text" name="answer" />')
        


class TrueFalseQuestion(models.Model):
    question_text = models.CharField(max_length=500)
    correct_answer = models.BooleanField()

    def __str__(self):
        return self.question_text

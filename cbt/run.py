#from cbt.models import Course, Question, Option 
import json
with open("essays.json") as f:
    #co = Course.objects.create(name="English test")
    js = json.load(f)
    for q in js:
        #qu = Question.objects.create(question=q.question)
        print(q)
        for op in q.get("options"):
            print(op)
        #    o = Option.objects.create(value=op)
#            qu.options.add(o)
#            if q.answer == op:
#                qu.answer = o
#            qu.save()
#        co.questions.add(qu)
#        co.save()
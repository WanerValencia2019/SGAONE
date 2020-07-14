import json
from django.shortcuts import render,get_object_or_404,reverse,redirect
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse,JsonResponse
from django.core import serializers
from django.views.generic import ListView,DetailView,FormView,UpdateView,DeleteView
from django.views import View


from .models import Subject,Course,Teacher,Student
from apps.activities.forms import AssignmentForm
from apps.activities.models import Assignment,Question,Answer,GradedAssignment,Choice

# Create your views here.

"""def get_subjects(request):
    queryset=Subject.objects.all()
    
    serialized=serializers.serialize("json",Subject.objects.all())
    
    return JsonResponse(serialized,safe=False)"""
    
@require_http_methods('GET',)    
def teacher_home(request):
    #print(request.user)
    teacher=Teacher.objects.only('id','teacher_subjecs','teacher_course').get(user=request.user)
    assignments=Assignment.objects.filter(teacher=teacher).select_related()[:5]
    print(teacher)
    subjects=teacher.teacher_subjecs.all()[:5]
    courses=teacher.teacher_course.all()[:5]
    return render(request,"teacher/home.html",{'courses':courses,'subjects':subjects,'assignments':assignments})

@require_http_methods(['GET','POST','PUT']) 
def teacher(request):
    teacher=Teacher.objects.get(user=request.user)
    return render(request,"teacher/account.html",{'account':teacher})
    

class TeacherCourses(ListView):
    context_object_name="courses"
    template_name="teacher/courses.html"
    
    def get_queryset(self):
        teacher=Teacher.objects.get(user_id=self.request.user.id)
        courses=teacher.teacher_course.all()
        return courses

class TeacherAssigment(ListView):
    queryset=Assignment.objects.all()
    context_object_name="assignments"
    template_name="teacher/assignment.html"
    
    def get_queryset(self):
        queryset = Assignment.objects.select_related('teacher','course').filter(teacher__user_id=self.request.user.id)
        return queryset
    
@require_http_methods('POST',)
def createChoices(request):    
    data = json.loads(request.body)
    assignment = data.get('id')
    choices = data.get('choices')
    title = data.get('title')
    answers = data.get('answers')
    obj_choices = []
    print(assignment)
    for choice in choices:
        print(choice)
    
    print(answers)
    for d in range(0,len(choices)):
        create = Question()
        create.question = title[d]
        create.assignment_id = int(assignment)
        #recorriendo las key de cada choice
        for key in choices[d].keys():
            #print(key)
            obj_choices.append(Choice(title='%s'%key))
        create.save()        
        ch=Choice.objects.bulk_create(obj_choices)
        obj_choices=[]
        #obteniendo y asignando las choices
        for c in ch:
            print(d)
            try:
                create.choices.add(Choice.objects.get(title=c))
            except Exception:
                create.choices.add(Choice.objects.filter(title=c)[0])
        create.answer_id= Choice.objects.get(title=answers[d]).id
        create.save()

    return JsonResponse([{'message':'created'}],safe=False)

@require_http_methods('POST',)
def createAssigment(request):    
    data = json.loads(request.body)
    print(request.data)
    objects = []
    print(type(data))
    for choice in data:
        for key in choice.keys():
            print(key)
            objects.append(Choice(title='%s'%key))
    print(objects)
    Choice.objects.bulk_create(objects)
    return JsonResponse([{'message':'created'}],safe=False)
    

class TeacherAssigmentCreate(FormView):
    form_class=AssignmentForm
    template_name="teacher/assignmentCreate.html"
    success_url='/sga/teacher/assignments'
    
    def post(self,request,*args, **kwargs):
        form=self.get_form_class()(request.POST)
        if form.is_valid():    
            form.save()
            return redirect(self.get_success_url())
        return super().get(request,args,kwargs)
    
    def get(self,request,*args, **kwargs):
        teacher=Teacher.objects.get(user_id=request.user.id)
        
        form=self.get_form_class()(initial={'teacher':teacher})
        
        return render(request,self.get_template_names(),{'form':form})
    
class TeacherAssignmentUpdate(UpdateView):
    queryset=Assignment.objects.all()
    form_class= AssignmentForm
    template_name="teacher/assignmentEdit.html"
    success_url='/sga/teacher/assignments'
    
    def get_object(self):
        queryset=Assignment.objects.get(id=self.kwargs.get('pk'))
        return queryset 
    
    def get(self,request,*args, **kwargs):
        form=self.get_form_class()(instance=self.get_object())
        return render(request,self.get_template_names(),{'form':form})
    
    def post(self,request,*args, **kwargs):
        form = self.get_form_class()(request.POST,instance=self.get_object())
        get=self.get_form_class()(instance=self.get_object())
        print(form.is_valid)
        if form.is_valid():
            form.save()
            return redirect('/sga/teacher/assignments')
        return render(request,self.get_template_names(),{'form':get})
        
class TeacherAssignmentDelete(DeleteView):
    model=Assignment
    template_name="teacher/deleteAssigment.html"
    success_url='/sga/teacher/assignments'
    context_object_name="assignment"
    
class TeacherGradedAssignment(ListView):
    queryset=Assignment.objects.all()
    context_object_name="teacher_assigment"
    template_name="teacher/gradedAssigment.html"

    def get_queryset(self):
        queryset = Assignment.objects.select_related().get(teacher__user=self.request.user)
        return queryset        
    
    def get(self,request,*args, **kwargs):
        courses = Teacher.objects.get(user=request.user)
        
        if request.is_ajax():
            course=request.GET['course']
            assignment=request.GET['assignment']
            data=[]
            print(assignment)
            gradedAssigment=GradedAssignment.query.get_course_assigment_teacher(course,assignment,request.user)

            for graded in gradedAssigment:
              item = {}
              item['id']=graded.student.id
              item['first_name']=graded.student.first_name
              item['last_name']=graded.student.first_name
              item['course']=graded.student.student_course.course
              item['assignment']=graded.assignment.title
              item['graded']=graded.grade
              data.append(item)
                
            print(json.dumps(data))
            serialized=serializers.serialize("json",gradedAssigment)
            return HttpResponse(json.dumps(data),'application/json')
        else:
            return render(request,"teacher/gradedAssigment.html",{'courses':courses})

def getAssigmentCourse(request):
    course=request.GET['course']
    assignments = Assignment.objects.select_related().filter(teacher__user=request.user,course__course=course)
    print(assignments)
    serialized=serializers.serialize("json",assignments,fields=('title'))
    return HttpResponse(serialized,'application/json')
    
    
class QuestionAssignment(ListView):
    template_name="teacher/questionAssignment.html"
    context_object_name="questionsAssigment"
    
    def get_queryset(self):
        teacher=Teacher.objects.select_related().values('id').get(user=self.request.user)
        title=self.kwargs.get('title')
        question=Question.objects.filter(assignment__teacher_id=teacher.get('id'),assignment__title=title).select_related('answer','assignment')
        print(self.kwargs.get('title'))
        
        return question

class StudentCourse(View):
    template_name="teacher/studentCourse.html"
    #context_object_name="studentsCourse"
    
    def get(self,request,*args, **kwargs):
        course=kwargs.get('course')
        students=Student.objects.select_related('student_course').filter(student_course__course=course).order_by('first_name')
        print(students)
        
        return render(request,self.template_name,{'studentsCourse':students,'course':course})

class StudentDetailTeacher(DetailView):
    model=Student
    template_name="teacher/detailStudent.html"
    context_object_name="student"
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        teacher=Teacher.objects.select_related().values('id').get(user=self.request.user)
        #print(teacher)
        student=self.get_object()
        answer=GradedAssignment.query.select_related().filter(student=student,assignment__teacher_id=teacher.get('id'))
        context['answers']=answer
        return context


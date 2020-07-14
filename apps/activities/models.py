from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.db.models import F, Q
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.shortcuts import redirect, reverse

from apps.gestor.models import Course, Student, Teacher
from .managers import  GradedAssigmentManager
# Create your models here.

class Assignment(models.Model):
    ACTIVE='ACTIVE'
    CLOSED='CLOSED'
    WAIT='WAIT'
    STATUS = [
        (ACTIVE, 'Activo'),
        (CLOSED, 'Cerrado'),
        (WAIT,'Esperando para inicio')
    ]
    title=models.CharField(max_length=100,verbose_name="Titúlo")
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE,verbose_name="Docente")
    course=models.ForeignKey(Course,on_delete=models.CASCADE,verbose_name="Curso")
    status=models.CharField(choices=STATUS,default=WAIT,max_length=6,verbose_name="Estado",null=True)
    created=models.DateTimeField(auto_now_add=True,verbose_name="Creado",null=True)
    start=models.DateField(verbose_name="Inicio",null=True)
    deadline=models.DateTimeField(verbose_name="Fecha de entrega",null=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("detail-assigment-questions",kwargs={'title':self.title})
    
    def get_count_questions(self):
        count = Question.objects.select_related('assignment').filter(assignment_id=self.pk).count()
        return count
    
    class Meta:
        verbose_name="Examen"
        verbose_name_plural="Examenes"
        
class GradedAssignment(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE,verbose_name="Alumno")
    assignment=models.ForeignKey(Assignment,on_delete=models.CASCADE,verbose_name="Examen")
    grade=models.FloatField(verbose_name="Calificación",default=0)
    query=GradedAssigmentManager()
    def get_absolute_url(self):
        return reverse("detail-graded", kwargs={"id": self.id})
    
    def __str__(self):
        return "{} ---- {} ----- {}".format(self.get_fullName(),self.assignment.teacher,self.grade)
    
    def get_fullName(self):
        return "{} {}".format(self.student.first_name,self.student.last_name)
    
    def get_correct_answer(self):
        count=Answer.objects.select_related().filter(correct_answer=True,student__id=self.student.id,question__assignment=self.assignment).count()
        return count
    
    def get_incorrect_answer(self):
        count=Answer.objects.select_related().filter(correct_answer=False,student__id=self.student.id,question__assignment=self.assignment).count()
        return count
    
    def get_total_answer(self):
        count=Answer.objects.select_related().filter(student__id=self.student.id,question__assignment=self.assignment).count()
        return "{}/10".format(count)
    
    class Meta:
        verbose_name="Calificación"
        verbose_name_plural="Calificaciones"
        
class Choice(models.Model):
    title=models.CharField(max_length=100,verbose_name="Item")

    def get_absolute_url(self):
        return reverse("detail-choice", kwargs={"id": self.id})
    
    def __str__(self):
        return self.title
    class Meta:
        verbose_name="Item"
        verbose_name_plural="Items"
        
class Question(models.Model):
    question=models.CharField(max_length=200,verbose_name="Pregunta")
    choices=models.ManyToManyField(Choice,verbose_name="Respuestas",related_name="choices")
    answer=models.ForeignKey(Choice,on_delete=models.CASCADE,verbose_name="Respuesta correcta",related_name="question_answer",null=True)
    assignment=models.ForeignKey(Assignment,on_delete=models.CASCADE,verbose_name="Examen",related_name="questions")
    grade=models.FloatField(verbose_name="Valor de la pregunta[0.5]",default=0.5,null=True)
    created=models.DateTimeField(auto_now_add=True,verbose_name="Creada",null=True)
    
    def get_absolute_url(self):
        return reverse("detail-question", kwargs={"id": self.id})
    
    def  __str__(self):
        return self.question
    
    class Meta:
        verbose_name="Pregunta"
        verbose_name_plural="Preguntas"
    
class Answer(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE,verbose_name="Estudiante",related_name="answer_student")
    question=models.ForeignKey(Question,on_delete=models.CASCADE,verbose_name="Pregunta",related_name="answer_question")
    answer=models.ForeignKey(Choice,on_delete=models.CASCADE,verbose_name="Respuesta",related_name="answer_resolved")
    correct_answer=models.BooleanField(verbose_name="Respuesta correcta",default=False,null=True,editable=False)
    resolved=models.BooleanField(verbose_name="Resuelta",default=False,null=True,editable=False)
    
    def get_absolute_url(self):
        return reverse("detail-answer", kwargs={"id": self.id})
    
    def __str__(self):
        return "{} {}".format(self.student.first_name,self.student.last_name)
    
    

    class Meta:
        verbose_name="Respuesta"
        verbose_name_plural="Respuestas"


@receiver(pre_save,sender=Answer)
def validate(sender,instance,**kwargs):
    question=instance.question.question
    student=instance.student
    print("PRE SAVE ANSWER")
    exist=Answer.objects.filter(Q(student_id=student.id) & Q(question__question=question)).exists()    
    print("PRE_SAVE {}".format(kwargs))
    if exist and not kwargs.get('created'):
        raise ValidationError(f"Esta pregunta ya ha sido respondida por {student.first_name}")
        
@receiver(post_save,sender=Answer)
def add_qualification(sender,instance,**kwargs):
    print("POST SAVE ANSWER")
    question=instance.question.question
    assignment=instance.question.assignment
    student=instance.student
    answer_correct=instance.question.answer
    answer=instance.answer
    exist=Answer.objects.filter(Q(student_id=student.id) & Q(question__assignment=assignment)).exists()
    print(exist)
    #print(assignment.id)
    #print(dir(instance))
    #print(kwargs)
    if exist==True and not kwargs.get('created'):
            raise ValidationError(f"Esta pregunta ya ha sido respondida por {student.first_name}")
        
    if exist==True and not kwargs.get('created') and instance.resolved:
            raise ValidationError(f"Esta pregunta ya ha sido respondida por {student.first_name}")
        
    if answer==answer_correct:
        #print(evaluation)
            print("PRIMERA {}".format(instance))
            graded_save_update(student,assignment,0.5)
            Answer.objects.filter(Q(student_id=student.id) & Q(question__question=question)).update(resolved=True,correct_answer=True)    
    else:
            print("SEGUNDA {}".format(instance))
            graded_save_update(student,assignment)
            Answer.objects.filter(Q(student_id=student.id) & Q(question__question=question)).update(resolved=True,correct_answer=False)
    
def graded_save_update(student,assignment=None,value=0):
    try:
        graded=GradedAssignment.query.get(student=student,assignment_id=assignment.id)
        graded.grade=F('grade')+value
        graded.save() 
        #print(graded)
        #instance.resolved=True
        #instance.save()
        print("ACTUALIZANDO {}".format(graded))
    except ObjectDoesNotExist:
            graded=GradedAssignment()  
            print(dir(graded) )
            graded.student_id=student.id
            graded.assignment_id=assignment.id
            graded.grade=value
            graded.save()
            print("CREANDO {}".format(graded))
            #instance.resolved=True
            #instance.save()

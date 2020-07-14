from os.path import join, split

from django.shortcuts import reverse
from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _

from .managers import QualificationManager



# Create your models here.

class PropertyUser(models.Model):
    FEMALE='FM'
    MALE='MA'
    GENDER = [
        (FEMALE, 'Femenino'),
        (MALE, 'Masculino'),
    ]
    
    id=models.CharField(verbose_name="Identificación",max_length=11,primary_key=True,blank=False,db_index=True,)
    first_name=models.CharField(verbose_name="Nombre",max_length=100)
    last_name=models.CharField(verbose_name="Apellidos",max_length=100)
    gender = models.CharField(
        max_length=2,
        choices=GENDER,
        default=None,
        null=True,
        blank=True,
        verbose_name="Género"
    )
    created_at=models.DateTimeField(auto_now_add=True,verbose_name="Creado",null=True)
    update_at=models.DateField(auto_now=True,verbose_name="Actualizado",null=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE,verbose_name="Perfil",null=True)
    class Meta:
       abstract = True
       

class Subject(models.Model):
    subject=models.CharField(verbose_name="Asignatura",max_length=100,blank=False)
    
    def __str__(self):
        return self.subject 
    
    class Meta:
        verbose_name = 'Asignatura'
        verbose_name_plural = 'Asignaturas'
        ordering=['-id']
    
class Course(models.Model):
    course=models.CharField(verbose_name="Nombre del curso",max_length=100)
    course_subject=models.ManyToManyField(Subject,verbose_name="Asignaturas",related_name="course_subject")
    
    def __str__(self):
        return "{}".format(self.course,)
    
    def get_absolute_url(self):
        return reverse("students-course", kwargs={"course": self.course})
    
    def get_students(self):
        count=Student.objects.filter(student_course_id=self.pk).count()
        return count
    
    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering=['-id']
        
class Student(PropertyUser):
    student_course=models.ForeignKey(Course,on_delete=models.CASCADE,verbose_name="Curso",related_name="student_course")
    
    def __str__(self):
        return "{}-{}-{}".format(self.id,self.get_fullName(),self.student_course)
    
    def get_fullName(self):
        return "{} {}".format(self.first_name,self.last_name)
    
    def get_absolute_url(self):
        return reverse('detail-student-teacher', kwargs={'course':self.student_course.course,'pk': self.pk})
    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'
        ordering=['-id']
        
def create_profile_student(sender,instance,**kwargs):
    #print(instance.objects)
    first_name,last_name=instance.first_name,instance.last_name
    #print(dir(first_name))
    if instance.user_id!=None:
        print("SE HA actualizado el usuario")
        #group=Group.objects.get(name="Estudiante")
        #print(group.id)
        #user=User.objects.select_related().get(pk=1)
        #print(dir(user.groups))
        #user.groups.set([group])
        #print(user.groups)
    else:
        email=first_name.split(" ")[0][:3].lower()+last_name.split(" ")[0].lower()+"@sgaone.edu.co"
        username=first_name[:3].lower()+last_name.split(" ")[0].lower()
        password="SGAONE2020"
        #print(dir(create_user))
        group=Group.objects.get(name="Estudiante")
        create_user=User()
        
        create_user.username=username
        create_user.first_name=first_name
        create_user.last_name=last_name
        create_user.email=email
        create_user.set_password(password)
        create_user.save()
        create_user.groups.set([group])
        
        instance.user=create_user
        instance.save()        
    #print(instance)
    
post_save.connect(create_profile_student,sender=Student)
    
class Teacher(PropertyUser):
    teacher_subjecs=models.ManyToManyField(Subject,verbose_name="Asignaturas",related_name="teacher_subjects")
    teacher_course=models.ManyToManyField(Course,verbose_name="Cursos",related_name="teacher_course")
    def __str__(self):
        return "{} {}".format(self.first_name,self.last_name)
    
    class Meta:
        verbose_name = 'Docente'
        verbose_name_plural = 'Docentes'
        ordering=['-id']

def create_profile_teacher(sender,instance,**kwargs):
    #print(instance.objects)
    first_name,last_name=instance.first_name,instance.last_name
    #print(dir(first_name))
    if instance.user_id!=None:
        print("SE HA actualizado el usuario")
    else:
        email=first_name.split(" ")[0].lower()+"."+last_name.split(" ")[0].lower()+"@sgateacher.edu.co"
        username=first_name.split(" ")[0].lower()+last_name.split(" ")[0].lower()
        password="SGAONE2020"
        #print(dir(create_user))
        group=Group.objects.get(name="Docente")
        create_user=User()
        
        create_user.username=username
        create_user.first_name=first_name
        create_user.last_name=last_name
        create_user.email=email
        create_user.set_password(password)
        create_user.save()
        create_user.groups.set([group])
        
        instance.user=create_user
        instance.save()        
    #print(instance)
    
post_save.connect(create_profile_teacher,sender=Teacher)



def validate_qualification(value):
        print(value)
        if not (value > 0 and value<=5):
            raise ValidationError(
                _('%(value) no tiene el formato correcto debe estar entre [0-5]'),
                params={'value': value},
            )
        else:
            return True
    
class Qualification(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE,verbose_name="Estudiante",related_name="student_qualification")
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE,verbose_name="Asignaturas",related_name="subject_qualificaction")
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE,verbose_name="Docente",related_name="teacher_qualification")
    qualification=models.FloatField(verbose_name="Calificación",null=True,validators=[validate_qualification,])
    objects=QualificationManager()
    def __str__(self):
        return "{} {}".format(self.student,self.subject)
    
    class Meta:
        verbose_name = 'Calificación'
        verbose_name_plural = 'Calificaciones'
        ordering=('student',)

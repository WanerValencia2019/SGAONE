from django.contrib import admin
from .models import *
# Register your models here.


admin.AdminSite.site_header="SGA ONE"
admin.AdminSite.site_title="SITIO ADMINISTRATIVO SGA ONE"


class SubjectAdmin(admin.ModelAdmin):
    list_display=('subject',)
    search_fields=('subject',)
    list_per_page=15
    def get_readonly_fields(self,request,obj):
        user=request.user
        #print(dir(user.groups.filter(name="Docente")))
        if user.groups.filter(name="Docente").exists():
            return ["subject",]
        return []
    

class CourseAdmin(admin.ModelAdmin):
    fields=('course','course_subject',)
    list_display=('course',)
    list_filter=('course','course_subject',)
    list_per_page=15
    ordering=('course',)
    search_fields=('course','course_subject__subject')
    filter_horizontal=('course_subject',)
    
   
class StudentAdmin(admin.ModelAdmin):
    date_hierarchy="created_at"
    list_display=['id','first_name','last_name','student_course','user']
    list_display_links = ('id',)
    list_filter=('id','student_course')
    list_select_related=('student_course',)
    ordering=("first_name","id","created_at",)
    search_fields=("id","first_name","last_name")
    list_per_page=15
    fields=('id',('first_name','last_name'),'student_course','gender')
    
    """def get_fields(self,request,obj):
        print(request.user)
        
        return ['id',"first_name"]"""
    
    """def get_course(self,obj):
        print(obj.student_course.course)
        return obj.student_course.course
    get_course.eempty_value_display = 'unknown'"""
    
class TeacherAdmin(admin.ModelAdmin):
    fields=('id',('first_name','last_name'),'teacher_subjecs','teacher_course','gender')
    list_display=('id','nombre_completo','user')
    list_display_links=('id','nombre_completo',)
    list_filter=('teacher_course','teacher_subjecs',)
    filter_horizontal=('teacher_subjecs','teacher_course',)
    
    def nombre_completo(self,obj):
        return "{0} {1}".format(obj.first_name,obj.last_name)
    
    nombre_completo.eempty_value_display = 'Desconocido'
    
class QualificationAdmin(admin.ModelAdmin):
    #fields=('student','subject','')
    list_display=('nombre_completo','subject','teacher','qualification')
    list_filter=('subject','teacher',)
    list_display_links=('nombre_completo','subject')
    list_per_page=20
    search_fields=('nombre_completo','subject','teacher')
    def nombre_completo(self,obj):
        return "{0} {1}".format(obj.student.first_name,obj.student.last_name)
    
    nombre_completo.eempty_value_display = 'Desconocido'

admin.site.register(Subject,SubjectAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(Teacher,TeacherAdmin)
admin.site.register(Qualification,QualificationAdmin)
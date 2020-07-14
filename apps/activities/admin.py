from django.contrib import admin
from .models import Answer, Assignment, Choice, GradedAssignment, Question

# Register your models here.

class ChoiceAdmin(admin.ModelAdmin):
    list_display=('title',)
    #list_filter=('title',)
    search_fields=('title',)
    list_per_page=15

class QuestionAdmin(admin.ModelAdmin):
    list_display=('question','answer','assignment','docente','grade',)
    list_filter=('assignment__teacher',)
    search_fields=('question','docente')
    filter_horizontal=('choices',)
    def docente(self,obj):
        return "{}".format(obj.assignment.teacher)    
    
    docente.eempty_value_display = 'Desconocido'

class AssignmentAdmin(admin.ModelAdmin):
    list_display=('title','teacher','course','status','start','deadline')
    list_filter=('course__course',)
    search_fields=('course__course','teacher__first_name','teacher__last_name')

class GradedAdmin(admin.ModelAdmin):
    list_display=('alumno','assignment','grade')
    list_display_links=list_display
    list_filter=('assignment__title',)
    search_fields=('student__first_name','assignment__title')
    
    def alumno(self,obj):
        return "{}".format(obj.student.get_fullName())    
    
    alumno.eempty_value_display = 'Desconocido'

class AnswerAdmin(admin.ModelAdmin):
    list_display=('alumno','question','answer','resolved','correct_answer')

    def alumno(self,obj):
        return "{}".format(obj.student.get_fullName())    
    
    alumno.eempty_value_display = 'Desconocido'
admin.site.register(Choice,ChoiceAdmin)
admin.site.register(Question,QuestionAdmin)
admin.site.register(Assignment,AssignmentAdmin)
admin.site.register(GradedAssignment,GradedAdmin)
admin.site.register(Answer,AnswerAdmin)

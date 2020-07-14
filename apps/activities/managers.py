from django.db.models import Manager



class GradedAssigmentManager(Manager):
    def get_queryset(self):
        queryset = super(GradedAssigmentManager, self).get_queryset()
        queryset = queryset 
        return queryset
    
    def get_course_assigment_teacher(self,course,assigment,teacherUser=None):
        return self.get_queryset().filter(student__student_course__course=course,assignment__title=assigment,assignment__teacher__user=teacherUser)
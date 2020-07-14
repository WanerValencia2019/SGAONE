from django.db import models


class QualificationManager(models.Manager):
    def get_queryset(self):
        queryset = super(QualificationManager, self).get_queryset()
        queryset = queryset 
        return queryset
    
    def reprobate_students_course(self,course):
        return self.get_queryset().filter(qualification__lt=3,student__student_course__course=course)
    
    def approved_students_course(self,course):
        return self.get_queryset().filter(qualification__gte=3,student__student_course__course=course)
    
    def reprobate_subcour(self,subject,course):
        return self.get_queryset().filter(qualification__lt=3,subject__subject=subject,student__student_course__course=course)
    
    def approved_subcour(self,subject,course):
        return self.get_queryset().filter(qualification__gte=3,subject__subject=subject,student__student_course__course=course)
    
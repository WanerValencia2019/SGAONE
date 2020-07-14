from django.urls import path
from .views import *

urlpatterns = [
    #path('',get_subjects,name="all")
    path('teacher/home',teacher_home,name="teacher-home"),
    path('teacher/account',teacher,name="teacher-account"),
    path('teacher/courses',TeacherCourses.as_view(),name="teacher-courses"),
    path('teacher/assignments',TeacherAssigment.as_view(),name="teacher-assigment"),
    path('teacher/choices',createChoices,name="teacher-choices"),
    path('teacher/assignments/create',TeacherAssigmentCreate.as_view(),name="teacher-assigment-create"),
    path('teacher/assigments/edit/<int:pk>/',TeacherAssignmentUpdate.as_view(),name="teacher-assigment-update"),
    path('teacher/assigments/delete/<int:pk>/',TeacherAssignmentDelete.as_view(),name="teacher-assigment-delete"),
    path('teacher/gradedAssigment/',TeacherGradedAssignment.as_view(),name="teacher-graded-assigment"),
    path('teacher/gradedAssigment/assignment/',getAssigmentCourse,name="graded-course-assigments"),
    path('teacher/assignments/<title>/questions',QuestionAssignment.as_view(),name="detail-assigment-questions"),
    path('teacher/courses/<course>',StudentCourse.as_view(),name="students-course"),
    path('teacher/courses/<course>/<int:pk>',StudentDetailTeacher.as_view(),name="detail-student-teacher"),
    
]



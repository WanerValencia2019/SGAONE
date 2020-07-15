from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    #path('',get_subjects,name="all")
    path('teacher/home',login_required(teacher_home,login_url='login'),name="teacher-home"),
    path('teacher/account',login_required(teacher,login_url='login'),name="teacher-account"),
    path('teacher/courses',login_required(TeacherCourses.as_view(),login_url='login'),name="teacher-courses"),
    path('teacher/assignments',login_required(TeacherAssigment.as_view(),login_url='login'),name="teacher-assigment"),
    path('teacher/choices',login_required(createChoices,login_url='login'),name="teacher-choices"),
    path('teacher/assignments/create',login_required(TeacherAssigmentCreate.as_view(),login_url='login'),name="teacher-assigment-create"),
    path('teacher/assigments/edit/<int:pk>/',login_required(TeacherAssignmentUpdate.as_view(),login_url='login'),name="teacher-assigment-update"),
    path('teacher/assigments/delete/<int:pk>/',login_required(TeacherAssignmentDelete.as_view(),login_url='login'),name="teacher-assigment-delete"),
    path('teacher/gradedAssigment/',login_required(TeacherGradedAssignment.as_view(),login_url='login'),name="teacher-graded-assigment"),
    path('teacher/gradedAssigment/assignment/',login_required(getAssigmentCourse,login_url='login'),name="graded-course-assigments"),
    path('teacher/assignments/<title>/questions',login_required(QuestionAssignment.as_view(),login_url='login'),name="detail-assigment-questions"),
    path('teacher/courses/<course>',login_required(StudentCourse.as_view(),login_url='login'),name="students-course"),
    path('teacher/courses/<course>/<int:pk>',login_required(StudentDetailTeacher.as_view(),login_url='login'),name="detail-student-teacher"),
    
]



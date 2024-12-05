from django.contrib import admin
from .models import Teacher, Student, Course, Subject, Classroom, Attendance, GPA, Grade
from django.db import models


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher_id', 'teacher_name', 'designation')  # Customize fields to be displayed
    search_fields = ('teacher_id', 'teacher_name')  # Add search functionality


class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'student_name', 'batch')
    search_fields = ('student_id', 'student_name')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'course_name')
    search_fields = ('course_id', 'course_name')


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_id', 'subject_name', 'student')  # Includes foreign key dropdown for student
    list_filter = ('student',)  # Filter subjects based on the student
    search_fields = ('subject_id', 'subject_name', 'student__student_name')  # Search based on related student


class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('classroom_id', 'teacher', 'subject')  # Includes foreign key dropdowns for teacher and subject
    search_fields = ('classroom_id', 'teacher__teacher_name', 'subject__subject_name')  # Search based on related teacher and subject
    list_filter = ('teacher', 'subject')  # Filter classrooms based on teacher and subject


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('attendance_id', 'current_date', 'student', 'classroom')  # Includes foreign key dropdowns for student and classroom
    list_filter = ('student', 'classroom')  # Filter based on student and classroom
    search_fields = ('student__student_name', 'classroom__classroom_id')  # Search by student and classroom


class GPAAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'grade', 'gpa', 'semester')
    search_fields = ('student__student_name', 'course__course_name')
    list_filter = ('semester',)


class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'teacher', 'grade')  # Includes foreign key dropdowns for student, course, and teacher
    search_fields = ('student__student_name', 'course__course_name', 'teacher__teacher_name')
    list_filter = ('course', 'teacher')


# Register your models
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(GPA, GPAAdmin)
admin.site.register(Grade, GradeAdmin)

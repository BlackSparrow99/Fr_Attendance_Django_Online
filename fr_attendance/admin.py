from django.contrib import admin
from .models import Teacher, Student, Course, Subject, StudentSubject, Classroom, Attendance, GPA, Grade


# TeacherAdmin
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher_id', 'teacher_name', 'designation')  # Customize fields to be displayed
    search_fields = ('teacher_id', 'teacher_name')  # Add search functionality


# StudentAdmin
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'student_name', 'batch')
    search_fields = ('student_id', 'student_name')


# CourseAdmin
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'course_name')
    search_fields = ('course_id', 'course_name')


# SubjectAdmin
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_id', 'subject_name')  # Removed student
    search_fields = ('subject_id', 'subject_name')  # Search by subject fields


# StudentSubjectAdmin
class StudentSubjectAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject')  # Displays student-subject relationships
    search_fields = ('student__student_name', 'subject__subject_name')  # Search through related fields
    list_filter = ('subject',)  # Filter by subject


# ClassroomAdmin
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('classroom_id', 'teacher', 'subject')  # Includes foreign key dropdowns for teacher and subject
    search_fields = ('classroom_id', 'teacher__teacher_name', 'subject__subject_name')  # Search based on related teacher and subject
    list_filter = ('teacher', 'subject')  # Filter classrooms based on teacher and subject


# AttendanceAdmin
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('attendance_id', 'current_date', 'student', 'classroom')  # Includes foreign key dropdowns for student and classroom
    list_filter = ('classroom', 'current_date')  # Filter based on classroom and date
    search_fields = ('student__student_name', 'classroom__classroom_id')  # Search by student and classroom


# GPAAdmin
class GPAAdmin(admin.ModelAdmin):
    list_display = ('student', 'semester', 'gpa')  # Display GPA for each student per semester
    search_fields = ('student__student_name', 'semester')  # Search by student and semester
    list_filter = ('semester',)  # Filter GPAs by semester


# GradeAdmin
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'teacher', 'grade', 'semester')  # Added semester to display
    search_fields = ('student__student_name', 'course__course_name', 'teacher__teacher_name', 'semester')  # Search by semester
    list_filter = ('course', 'teacher', 'semester')  # Filter by semester, course, and teacher


# Register your models
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(StudentSubject, StudentSubjectAdmin)  # Register StudentSubject
admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(GPA, GPAAdmin)
admin.site.register(Grade, GradeAdmin)

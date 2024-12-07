from django.contrib import admin
from django.utils.timezone import now
import os
from django.conf import settings
from .models import Teacher, Student, Course, Subject, StudentSubject, Classroom, Attendance, GPA, Grade
from .views import record_attendance_in_CSV


# TeacherAdmin
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher_id', 'teacher_name', 'designation', 'image')  # Display key teacher attributes including image
    search_fields = ('teacher_id', 'teacher_name')  # Search by teacher ID or name
    list_filter = ('designation',)  # Optionally, filter by designation (if useful)


# StudentAdmin
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'student_name', 'batch', 'course', 'image')  # Display key student attributes including image
    search_fields = ('student_id', 'student_name')  # Search by student ID or name
    list_filter = ('course',)  # Optionally, filter by course (if useful)


# CourseAdmin
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'course_name')  # Display course attributes
    search_fields = ('course_id', 'course_name')  # Search by course ID or name


# SubjectAdmin
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_id', 'subject_name')  # Display subject attributes
    search_fields = ('subject_id', 'subject_name')  # Search by subject ID or name


# StudentSubjectAdmin
class StudentSubjectAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'semester')  # Display student, subject, and semester
    search_fields = ('student__student_name', 'subject__subject_name', 'semester')  # Search by student, subject, or semester


# ClassroomAdmin
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('classroom_id', 'subject', 'teacher')  # Display classroom details
    search_fields = ('classroom_id', 'subject__subject_name', 'teacher__teacher_name')  # Search by classroom, subject, or teacher


class AttendanceAdmin(admin.ModelAdmin):

    list_display = ('student_id', 'name', 'classroom_id', 'recorded_date', 'attendance')  # Display attendance details
    list_filter = ('classroom_id', 'recorded_date', 'attendance')  # Filter by classroom, date, and attendance status
    search_fields = ('student_id__student_name', 'classroom_id__classroom_id')  # Search by student or classroom

    def save_model(self, request, obj, form, change):
        """
        Overrides save_model to handle additional logic for attendance.
        """
        # Save the attendance record
        super().save_model(request, obj, form, change)

        # Call the existing record_attendance_in_CSV function from views
        record_attendance_in_CSV(
            s_id=obj.student_id.student_id,
            classroom_id=obj.classroom_id.classroom_id
        )


# GPAAdmin
class GPAAdmin(admin.ModelAdmin):
    list_display = ('student', 'semester', 'gpa')  # Display student, semester, and GPA
    list_filter = ('semester',)  # Filter by semester
    search_fields = ('student__student_name', 'semester')  # Search by student or semester


# GradeAdmin
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'classroom', 'grade', 'semester', 'mark')  # Display grade details (now using Classroom)
    search_fields = ('student__student_name', 'classroom__subject__subject_name', 'classroom__teacher__teacher_name', 'semester')  # Search by student, subject, teacher
    list_filter = ('semester', 'classroom__subject', 'classroom__teacher')  # Filter by semester, subject, or teacher


# Register all models to be accessible in the admin interface
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(StudentSubject, StudentSubjectAdmin)
admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(GPA, GPAAdmin)
admin.site.register(Grade, GradeAdmin)

import os
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone


# Teacher model
class Teacher(models.Model):
    teacher_id = models.CharField(max_length=20, primary_key=True)
    teacher_name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)

    def __str__(self):
        return self.teacher_name


# Student model
class Student(models.Model):
    student_id = models.CharField(max_length=20, primary_key=True)
    student_name = models.CharField(max_length=255)
    batch = models.CharField(max_length=50)

    def __str__(self):
        return self.student_name


# Course model
class Course(models.Model):
    course_id = models.CharField(max_length=20, primary_key=True)
    course_name = models.CharField(max_length=255)

    def __str__(self):
        return self.course_name


# Subject model
class Subject(models.Model):
    subject_id = models.CharField(max_length=20, primary_key=True)
    subject_name = models.CharField(max_length=255)

    def __str__(self):
        return self.subject_name


# Student-Subject (Join Table for Many-to-Many)
class StudentSubject(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'subject')  # Composite key

    def __str__(self):
        return f"{self.student.student_name} enrolled in {self.subject.subject_name}"


# Classroom model
class Classroom(models.Model):
    classroom_id = models.CharField(max_length=20, primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)  # Link Classroom to Subject
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)  # Link Classroom to Teacher

    def __str__(self):
        return f"Classroom {self.classroom_id} for {self.subject.subject_name}"


# Attendance model
class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    current_date = models.DateField(default=timezone.now)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # Link Attendance to Student
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)  # Link Attendance to Classroom
    status = models.BooleanField(default=True)  # True for present, False for absent

    def __str__(self):
        return f"Attendance {self.attendance_id} for {self.student.student_name}"


# GPA model
class GPA(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # Link GPA to Student
    semester = models.CharField(max_length=20)  # Include semester field for GPA calculation per semester
    gpa = models.FloatField()  # GPA for that specific semester

    def __str__(self):
        return f"{self.student} - {self.semester}: {self.gpa}"


# Grade model
class Grade(models.Model):
    grade_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # Link Grade to Student
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Link Grade to Course
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)  # Link Grade to Teacher
    grade = models.CharField(max_length=2)
    semester = models.CharField(max_length=20)  # Added semester to track in which semester the grade is given

    def __str__(self):
        return f"{self.student.student_name}'s Grade in {self.course.course_name} ({self.semester}): {self.grade}"


# Signal to create a folder when a new classroom is created
@receiver(post_save, sender=Classroom)
def create_classroom_folder(sender, instance, created, **kwargs):
    if created:
        dataset_path = os.path.join(settings.MEDIA_ROOT, "Data_set", "Face_recognition", instance.classroom_id)
        os.makedirs(dataset_path, exist_ok=True)
        print(f"Folder created at: {dataset_path}")

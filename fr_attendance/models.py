import os
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone


class Teacher(models.Model):
    teacher_id = models.CharField(max_length=20, primary_key=True)
    teacher_name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)

    def __str__(self):
        return self.teacher_name


class Student(models.Model):
    student_id = models.CharField(max_length=20, primary_key=True)
    student_name = models.CharField(max_length=255)
    batch = models.CharField(max_length=50)

    def __str__(self):
        return self.student_name


class Course(models.Model):
    course_id = models.CharField(max_length=20, primary_key=True)
    course_name = models.CharField(max_length=255)

    def __str__(self):
        return self.course_name


class Subject(models.Model):
    subject_id = models.CharField(max_length=20, primary_key=True)
    subject_name = models.CharField(max_length=255)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject_name


class Classroom(models.Model):
    classroom_id = models.CharField(max_length=20, primary_key=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return f"Classroom {self.classroom_id}"


class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    current_date = models.DateField(default=timezone.now)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)  # True for present, False for absent

    def __str__(self):
        return f"Attendance {self.attendance_id}"


class GPA(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    grade = models.CharField(max_length=2)
    gpa = models.FloatField()
    semester = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.student} - {self.semester}: {self.gpa}"


class Grade(models.Model):
    grade_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.student.student_name}'s Grade: {self.grade}"


# Signal to create folder when a new classroom is created
@receiver(post_save, sender=Classroom)
def create_classroom_folder(sender, instance, created, **kwargs):
    if created:
        dataset_path = os.path.join(settings.MEDIA_ROOT, "Data_set", "Face_recognition", instance.classroom_id)
        os.makedirs(dataset_path, exist_ok=True)
        print(f"Folder created at: {dataset_path}")

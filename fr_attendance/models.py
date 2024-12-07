import os
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
from datetime import datetime


# Course model
class Course(models.Model):
    course_id = models.CharField(max_length=20, primary_key=True)
    course_name = models.CharField(max_length=255)

    def __str__(self):
        return self.course_name


# Teacher model
class Teacher(models.Model):
    teacher_id = models.CharField(max_length=20, primary_key=True)
    teacher_name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    image = models.ImageField(upload_to='Data_set/', null=True, blank=True)

    def __str__(self):
        return self.teacher_id

    def save(self, *args, **kwargs):
        if self.image:
            # Get the current image file name
            ext = self.image.name.split('.')[-1]  # Get file extension
            base_name = self.image.name.split('.')[0]  # Get base name without extension

            # Rename the image to include the teacher_id
            new_name = f"{self.teacher_id}_{base_name}.{ext}"
            self.image.name = os.path.join('Face_recognition', new_name)

        super().save(*args, **kwargs)


# Student model
class Student(models.Model):
    student_id = models.CharField(max_length=20, primary_key=True)
    student_name = models.CharField(max_length=255)
    batch = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Link Grade to Course
    image = models.ImageField(upload_to='Data_set/', null=True, blank=True)

    def __str__(self):
        return self.student_id

    def save(self, *args, **kwargs):
        if self.image:
            # Get the current image file name
            ext = self.image.name.split('.')[-1]  # Get file extension
            base_name = self.image.name.split('.')[0]  # Get base name without extension

            # Rename the image to include the student_id
            new_name = f"{self.student_id}_{base_name}.{ext}"
            self.image.name = os.path.join('Face_recognition', new_name)

        super().save(*args, **kwargs)


# Subject model
class Subject(models.Model):
    subject_id = models.CharField(max_length=20, primary_key=True)
    subject_name = models.CharField(max_length=255)

    def __str__(self):
        return self.subject_name


# Student-Subject (Join Table for Many-to-Many)
class StudentSubject(models.Model):
    SEMESTER_CHOICES = [
        ('1-1', '1st Year 1st Semester'),
        ('1-2', '1st Year 2nd Semester'),
        ('2-1', '2nd Year 1st Semester'),
        ('2-2', '2nd Year 2nd Semester'),
        ('3-1', '3rd Year 1st Semester'),
        ('3-2', '3rd Year 2nd Semester'),
        ('4-1', '4th Year 1st Semester'),
        ('4-2', '4th Year 2nd Semester'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    semester = models.CharField(max_length=5, choices=SEMESTER_CHOICES)  # Add semester with choices

    class Meta:
        unique_together = ('student', 'subject', 'semester')  # Composite key now includes semester

    def __str__(self):
        return f"{self.student.student_name} enrolled in {self.subject.subject_name} ({self.semester})"


# Classroom model
class Classroom(models.Model):
    classroom_id = models.CharField(max_length=20, primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)  # Link Classroom to Subject
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)  # Link Classroom to Teacher

    def __str__(self):
        return f"Classroom {self.classroom_id} for {self.subject.subject_name}"


# Attendance model
class Attendance(models.Model):
    ATTENDANCE_CHOICES = [
        ('Absent', 'Absent'),
        ('Present', 'Present'),
    ]
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)  # Student's unique identifier
    name = models.CharField(max_length=255, null=True, blank=True)  # Allow null values
    attendance = models.CharField(default="Absent", max_length=10, choices=ATTENDANCE_CHOICES)  # Set a default value for attendance
    classroom_id = models.ForeignKey(Classroom, on_delete=models.CASCADE)  # Classroom or lecture ID
    recorded_date = models.DateField(default=timezone.now)  # Automatically record only the current date

    def save(self, *args, **kwargs):
        # Automatically set the 'name' field to the student's name based on 'student_id'
        if not self.name:
            self.name = self.student_id.student_name
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Attendance: {self.student_id} in {self.classroom_id} on {self.recorded_date}"


# GPA model
class GPA(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # Link GPA to Student
    semester = models.CharField(max_length=5, choices=StudentSubject.SEMESTER_CHOICES)
    gpa = models.FloatField()  # GPA for that specific semester

    def __str__(self):
        return f"{self.student} - {self.semester}: {self.gpa}"


class Grade(models.Model):
    grade_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # Link Grade to Student
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    mark = models.FloatField()  # Add the mark field
    grade = models.CharField(max_length=2, blank=True)  # Grade will be automatically assigned based on mark
    semester = models.CharField(max_length=20, blank=True)  # Automatically populated semester

    def save(self, *args, **kwargs):
        # Automatically assign grade based on mark
        self.mark = round(Decimal(self.mark), 2)  # Round the mark to 2 decimal places
        
        # Automatically assign semester based on the current date
        if not self.semester:
            current_month = datetime.now().month
            if 1 <= current_month <= 5:
                self.semester = 'Spring'  # Assuming Spring semester is from January to May
            elif 6 <= current_month <= 8:
                self.semester = 'Summer'  # Assuming Summer semester is from June to August
            elif 9 <= current_month <= 12:
                self.semester = 'Fall'  # Assuming Fall semester is from September to December

        # Automatically assign grade based on mark
        if self.mark >= 80:
            self.grade = "A+"
        elif self.mark >= 75:
            self.grade = "A"
        elif self.mark >= 70:
            self.grade = "A-"
        elif self.mark >= 65:
            self.grade = "B+"
        elif self.mark >= 60:
            self.grade = "B"
        elif self.mark >= 55:
            self.grade = "B-"
        elif self.mark >= 50:
            self.grade = "C"
        elif self.mark >= 45:
            self.grade = "C-"
        elif self.mark >= 40:
            self.grade = "D"
        elif self.mark >= 30:
            self.grade = "E"
        else:
            self.grade = "F"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.student_name}'s Grade in {self.classroom.subject.subject_name} ({self.semester}): {self.grade} ({self.mark})"


# Signal to set student name in Attendance before save
@receiver(pre_save, sender=Attendance)
def set_student_name(sender, instance, **kwargs):
    if not instance.name:
        instance.name = instance.student_id.student_name


# # Signal to create a folder when a new classroom is created
# @receiver(post_save, sender=Classroom)
# def create_classroom_folder(sender, instance, created, **kwargs):
#     if created:
#         try:
#             dataset_path = os.path.join(settings.MEDIA_ROOT, "Data_set", "Face_recognition", instance.classroom_id)
#             os.makedirs(dataset_path, exist_ok=True)
#             print(f"Folder created at: {dataset_path}")
#         except Exception as e:
#             print(f"Error creating folder: {e}")

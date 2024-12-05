# Generated by Django 5.1.3 on 2024-12-05 06:18

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Classroom",
            fields=[
                (
                    "classroom_id",
                    models.CharField(max_length=20, primary_key=True, serialize=False),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "course_id",
                    models.CharField(max_length=20, primary_key=True, serialize=False),
                ),
                ("course_name", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "student_id",
                    models.CharField(max_length=20, primary_key=True, serialize=False),
                ),
                ("student_name", models.CharField(max_length=255)),
                ("batch", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Teacher",
            fields=[
                (
                    "teacher_id",
                    models.CharField(max_length=20, primary_key=True, serialize=False),
                ),
                ("teacher_name", models.CharField(max_length=255)),
                ("designation", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="GPA",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("grade", models.CharField(max_length=2)),
                ("gpa", models.FloatField()),
                ("semester", models.CharField(max_length=20)),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="fr_attendance.course",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="fr_attendance.student",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Attendance",
            fields=[
                ("attendance_id", models.AutoField(primary_key=True, serialize=False)),
                ("current_date", models.DateField(default=django.utils.timezone.now)),
                (
                    "classroom",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="fr_attendance.classroom",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="fr_attendance.student",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Subject",
            fields=[
                (
                    "subject_id",
                    models.CharField(max_length=20, primary_key=True, serialize=False),
                ),
                ("subject_name", models.CharField(max_length=255)),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="fr_attendance.student",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="classroom",
            name="subject",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="fr_attendance.subject"
            ),
        ),
        migrations.CreateModel(
            name="Grade",
            fields=[
                ("grade_id", models.AutoField(primary_key=True, serialize=False)),
                ("grade", models.CharField(max_length=2)),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="fr_attendance.course",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="fr_attendance.student",
                    ),
                ),
                (
                    "teacher",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="fr_attendance.teacher",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="classroom",
            name="teacher",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="fr_attendance.teacher"
            ),
        ),
    ]
from django.http import HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings
from .models import Student, Classroom, Attendance, StudentSubject
from .utils import FaceRecognitionAttendance
import os
from datetime import datetime


@login_required
def home_page(request):
    return render(request, "fr_attendance/user_home.html")


@login_required
def video_feed(request):
    return render(request, "fr_attendance/live-feed.html")


@login_required
def live_feed(request):
    if request.method == 'GET':
        context = {'has_error': False, "data": request.GET}

        classroom_id = request.GET.get("classroom_id")
        if not classroom_id:
            messages.add_message(request, messages.ERROR, "Classroom ID is required")
            context['has_error'] = True
            return render(request, "fr_attendance/live-feed.html", context)

        # Check if the classroom exists
        if not Classroom.objects.filter(classroom_id=classroom_id).exists():
            messages.error(request, "Classroom ID not valid!")
            context['has_error'] = True
            return render(request, "fr_attendance/live-feed.html", context)

        # Initialize the face recognition system
        face_recognition_system = FaceRecognitionAttendance(classroom_id)
        face_recognition_system.load_or_create_encodings()
        q_lty, mup = FaceRecognitionAttendance.render_distance("close")

        def gen():
            yield from face_recognition_system.start_recognition(q_lty, mup)

        messages.success(request, "Attendance started recording.")
        return StreamingHttpResponse(gen(), content_type='multipart/x-mixed-replace; boundary=frame')
    return render(request, "fr_attendance/live-feed.html")


@login_required
def manual_attendance(request):
    if request.method == "POST":
        classroom_id = request.POST.get("classroom_id")
        student_id = request.POST.get("student_id")
        status = request.POST.get("status") == "Present"  # Convert status to boolean

        # Record attendance in CSV file (your existing logic)
        record_attendance_in_CSV(student_id, classroom_id)

        # Record attendance in the database
        attendance_record = record_attendance_in_database(student_id, classroom_id, status)

        # Provide feedback to the user
        if attendance_record[0]:
            messages.success(request, attendance_record[1])
        else:
            messages.info(request, attendance_record[1])

    return render(request, "attendance/manual_attendance.html")


def record_attendance_in_database(student_id, classroom_id, status):
    # Fetch classroom and student objects
    classroom = get_object_or_404(Classroom, classroom_id=classroom_id)
    student = get_object_or_404(Student, student_id=student_id)

    # Get today's date
    today_date = timezone.now().date()

    # Check or create attendance record
    attendance, created = Attendance.objects.get_or_create(
        student_id=student,  # Correct foreign key field name
        classroom_id=classroom,  # Correct foreign key field name
        recorded_date=today_date,  # Date field for today's date
        defaults={"attendance": "Absent"}  # Default to "Absent" if not created
    )

    # Update attendance status
    attendance.attendance = "Present" if status else "Absent"
    attendance.save()

    # Provide feedback
    if created:
        return True, f"Attendance added for {student.student_name} in {classroom.classroom_id} on {today_date}."
    else:
        return False, f"Attendance updated for {student.student_name} in {classroom.classroom_id} on {today_date}."


def record_attendance_in_CSV(s_id, classroom_id):
    # Set the attendance path for the current classroom
    attendance_path = os.path.join(settings.MEDIA_ROOT, "Attendance", classroom_id)
    os.makedirs(attendance_path, exist_ok=True)
    current_date = datetime.now().strftime("%d-%m-%Y")
    file_path = os.path.join(attendance_path, f"{current_date}.csv")

    # Get students in the same subject of the given classroom
    students_list = get_students_in_same_subject(classroom_id)
    students_dict = {students[0]: students[1] for students in students_list}

    if s_id in students_dict:
        s_name = students_dict[s_id]

    # If the CSV file doesn't exist, create it with a header and initial entries
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write("ID,Name,Attendance,Date\n")
            for student_id, student_name in students_dict.items():
                f.write(f"{student_id},{student_name},Absent,{current_date}\n")

    # Read the existing CSV file and check if the student's attendance is already recorded
    updated = False
    with open(file_path, "r") as f:
        lines = f.readlines()

    # Open the file to write the updated attendance
    with open(file_path, "w") as f:
        f.write("ID,Name,Attendance,Date\n")  # Write the header again

        # Process each line, check if the student is already listed and update their status
        for line in lines[1:]:  # Skip the header row
            student_id = line.split(",")[0]
            if student_id == s_id:
                # If the student is found, mark attendance as "Present"
                f.write(f"{s_id},{s_name},Present,{current_date}\n")
                updated = True
            else:
                # Keep other student records unchanged
                f.write(line)

        # If the student was not found, append their attendance at the end
        if not updated:
            f.write(f"{s_id},{s_name},Present,{current_date}\n")
            print(f"\t{s_id} {s_name} recorded in attendance.")


def get_students_in_same_subject(classroom_id):
    try:
        classroom = Classroom.objects.get(classroom_id=classroom_id)
    except Classroom.DoesNotExist:
        return f"Classroom with ID {classroom_id} does not exist."
    student_subjects = StudentSubject.objects.filter(subject=classroom.subject)
    students_in_same_subject = student_subjects.values_list('student__student_id', 'student__student_name')
    return students_in_same_subject

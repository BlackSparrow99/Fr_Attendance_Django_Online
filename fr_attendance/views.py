from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Student, Classroom, Attendance
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import os
from django.conf import settings
from django.http import StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from .utils import FaceRecognitionAttendance
from django.utils import timezone



@login_required
def video_feed(request):
    return render(request, "fr_attendance/live-feed.html")


# def home_page(request):
#     return HttpResponse("Welcome to the home page!")
@login_required
def home_page(request):
    return render(request, "fr_attendance/user_home.html")


# @login_required
# def live_feed(request):
#     # Batch name for the dataset and attendance paths
#     classroom = "CSE_batch_41"

#     # Construct paths using settings.MEDIA_ROOT
    # dataset_path = os.path.join(settings.MEDIA_ROOT, "Data_set", "Face_recognition", classroom_id)
    # attendance_path = os.path.join(settings.MEDIA_ROOT, "Attendance", classroom_id)
    # encoded_file = os.path.join(settings.MEDIA_ROOT, "Data_set", "Face_recognition", classroom_id, "encoded_faces.pkl")

#     # Initialize the FaceRecognitionAttendance system
#     face_recognition_system = FaceRecognitionAttendance(dataset_path, attendance_path, encoded_file)

#     # Load or create encodings
#     face_recognition_system.load_or_create_encodings()

#     # Quality and multiplier settings for face recognition
#     q_lty, mup = FaceRecognitionAttendance.render_distance("close")  # You can change to "mid" or "far"

#     # Streaming video feed
#     def gen():
#         # Start the face recognition process and yield frames
#         yield from face_recognition_system.start_recognition(q_lty, mup)  # Yield from the generator returned by start_recognition()

#     # Return the streaming response for live feed
#     return StreamingHttpResponse(gen(), content_type='multipart/x-mixed-replace; boundary=frame')


@login_required
def live_feed(request):
    if request.method == 'GET':
        context = {'has_error': False, "data": request.GET}

        classroom_id = request.GET.get("classroom_id")
        if not classroom_id:
            messages.add_message(request, messages.ERROR, "Classroom ID is required")
            context['has_error'] = True

            return render(request, "fr_attendance/live-feed.html")
        elif not Classroom.objects.filter(classroom_id=classroom_id).exists():
            messages.error(request, "Classroom ID not valid!")
            context['has_error'] = True
            # return render(request, "fr_attendance/live-feed.html", {"error": "Classroom ID is required."})
        if context['has_error']:
            return render(request, "fr_attendance/live-feed.html", context)

        face_recognition_system = FaceRecognitionAttendance(classroom_id)
        face_recognition_system.load_or_create_encodings()
        q_lty, mup = FaceRecognitionAttendance.render_distance("close")
        # Streaming video feed

        def gen():
            yield from face_recognition_system.start_recognition(q_lty, mup)
        # Return the streaming response for live feed
        messages.success(request, "Attendance started recording.")
        return StreamingHttpResponse(gen(), content_type='multipart/x-mixed-replace; boundary=frame')
    return render(request, "fr_attendance/live-feed.html")


# Manual attendance view
@login_required
def manual_attendance(request):
    if request.method == "POST":
        classroom_id = request.POST.get("classroom_id")
        student_id = request.POST.get("student_id")
        status = request.POST.get("status") == "present"
        student = get_object_or_404(Student, student_id=student_id)
        classroom = get_object_or_404(Classroom, classroom_id=classroom_id)
        attendance, created = Attendance.objects.get_or_create(
            student=student, classroom=classroom, current_date=timezone.now()  # Using timezone.now()
        )
        attendance.status = status
        attendance.save()
        if created:
            messages.success(request, "Attendance added successfully.")
        else:
            messages.info(request, "Attendance updated successfully.")
    return render(request, "attendance/manual_attendance.html")

import threading
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from validate_email import validate_email
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from helpers.decorators import auth_user_should_not_access
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.decorators import login_required
from fr_attendance.models import Student, Teacher


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = "Activate your account"
    email_body = render_to_string("authentication/activate.html", {
        "user": user,
        "domain": current_site,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": generate_token.make_token(user)
    })
    email = EmailMessage(subject=email_subject, body=email_body, from_email=settings.EMAIL_FROM_USER, to=[user.email])
    EmailThread(email).start()


@auth_user_should_not_access
def register(request):
    if request.method == 'POST':
        context = {'has_error': False, "data": request.POST}
        username = request.POST.get('username')
        identifier = request.POST.get('identifier')  # Student ID or Teacher ID
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        # Validation
        if not username:
            messages.error(request, "Username is required!")
            context['has_error'] = True
        student_profile = None
        teacher_profile = None
        # Check for existing ID in User model
        if identifier:
            # Ensure the identifier isn't already registered
            if User.objects.filter(student_profile__student_id=identifier).exists():
                messages.error(request, "This ID is already registered!")
                context['has_error'] = True
            elif User.objects.filter(teacher_profile__teacher_id=identifier).exists():
                messages.error(request, "This ID is already registered!")
                context['has_error'] = True
            else:
                # Check if the identifier exists in Student or Teacher tables
                if Student.objects.filter(student_id=identifier).exists():
                    student_profile = Student.objects.get(student_id=identifier)
                elif Teacher.objects.filter(teacher_id=identifier).exists():
                    teacher_profile = Teacher.objects.get(teacher_id=identifier)
                else:
                    messages.error(request, "Invalid ID!")
                    context['has_error'] = True
        else:
            messages.error(request, "Identifier is required!")
            context['has_error'] = True
        if not email:
            messages.error(request, "Email is required!")
            context['has_error'] = True
        elif not validate_email(email):
            messages.error(request, "Invalid email address!")
            context['has_error'] = True
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            context['has_error'] = True
        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters!")
            context['has_error'] = True
        elif password != password2:
            messages.error(request, "Passwords do not match!")
            context['has_error'] = True
        # Return errors
        if context['has_error']:
            return render(request, "authentication/new_register.html", context)
        # Create user and assign profile
        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        if student_profile:
            user.is_staff = False
            user.is_student = True
            user.student_profile = student_profile
        elif teacher_profile:
            user.is_staff = True
            user.is_teacher = True
            user.teacher_profile = teacher_profile
        user.save()
        # Send activation email
        send_activation_email(user, request)
        messages.success(request, "We sent you an email to verify your account.")
        return redirect("login")
    return render(request, "authentication/new_register.html")


@auth_user_should_not_access
def resend_authentication(request):
    if request.method == 'POST':
        context = {'has_error': False, "data": request.POST}
        email = request.POST.get('email')
        username = request.POST.get('username')
        if not username:
            messages.add_message(request, messages.ERROR, "Username is required!")
            context['has_error'] = True
        if not email:
            messages.add_message(request, messages.ERROR, "Email address is required!")
            context['has_error'] = True
        elif not validate_email(email):
            messages.add_message(request, messages.ERROR, "Enter a valid email address!")
            context['has_error'] = True
        elif context['has_error']:
            messages.add_message(request, messages.WARNING, "Please provide valid information!")
            context['has_error'] = True
            return render(request, "authentication/new_resend_authentication.html", context)
        user = User.objects.get(username=username, email=email)
        if user.is_email_verified:
            messages.add_message(request, messages.INFO, "Email is already verified! Try to login.")
            return render(request, "authentication/login.html")
        send_activation_email(user, request)
        messages.add_message(request, messages.SUCCESS, "We sent you an email to verify your account.")
        return redirect("login")
    return render(request, "authentication/new_resend_authentication.html")


@auth_user_should_not_access
def login_user(request):
    if request.method == "POST":
        context = {"data": request.POST}
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if not user.is_email_verified:
                messages.add_message(request, messages.WARNING, "User email is not verified yet!")
                messages.add_message(request, messages.INFO, "Please provide email and e-mail.")
                return render(request, "authentication/new_resend_authentication.html")
            login(request, user)
            messages.add_message(request, messages.SUCCESS, f"Welcome {user.email}")
            return redirect(reverse("home"))
        else:
            messages.add_message(request, messages.ERROR, "Invalid credentials")
            return render(request, "authentication/new_login.html", context)
    return render(request, "authentication/new_login.html")


def logout_user(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, "Successfully logged out")
    return redirect(reverse("login"))


def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        user = None
    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()
        messages.add_message(request, messages.SUCCESS, "Email verified successfully, you can now login")
        return redirect(reverse("login"))
    return render(request, "authentication/activate-failed.html", {"user": user})


def delete_users(request):
    if request.method == "POST":
        username = request.POST.get("username")
        if username == "all_user":
            count, _ = User.objects.all().delete()
            messages.add_message(request, messages.SUCCESS, f"All {count} users have been successfully deleted.")
        else:
            users = User.objects.filter(username=username)
            count = users.delete()[0]
            if count > 0:
                messages.add_message(request, messages.SUCCESS, f"Username '{username}' has been successfully removed")
            else:
                messages.add_message(request, messages.ERROR, f'No user found with username "{username}"')
        return redirect(reverse("delete_users"))
    return render(request, "_partials/new_delete-user.html")


@login_required
def profile_view(request):
    current_user = request.user
    return render(request, 'profile.html', {'user': current_user})


@login_required
def admin_check_view(request):
    current_user = request.user

    if current_user.is_superuser:
        admin_status = "You are a superuser."
    elif current_user.is_staff:
        admin_status = "You are a staff member."
    else:
        admin_status = "You are a regular user."

    return render(request, 'admin_status.html', {
        'admin_status': admin_status,
        'user': current_user
    })


@login_required
def dashboard_view(request):
    user = request.user
    if user.is_student:
        return render(request, 'student_dashboard.html', {'user': user})
    elif user.is_teacher:
        return render(request, 'teacher_dashboard.html', {'user': user})
    elif user.is_superuser:
        return render(request, 'admin_dashboard.html', {'user': user})
    return render(request, 'dashboard.html', {'user': user})

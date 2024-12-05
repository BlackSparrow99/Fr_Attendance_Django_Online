from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # Override the username field to remove the unique constraint
    username = models.CharField(max_length=150)  # No unique=True here

    # Make email unique and set it as the username field for authentication
    email = models.EmailField(unique=True)

    # Custom fields for email verification and user types
    is_email_verified = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    # One-to-one relationships with the Student and Teacher models
    student_profile = models.OneToOneField(
        'fr_attendance.Student',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        unique=True,  # Ensures a user can only be linked to one student profile
        related_name="user_profile"
    )
    teacher_profile = models.OneToOneField(
        'fr_attendance.Teacher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        unique=True,  # Ensures a user can only be linked to one teacher profile
        related_name="user_profile"
    )

    # Override the USERNAME_FIELD to use email instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Email is now the username field

    # Permissions and access control logic
    def has_module_perms(self, app_label):
        # Prevent staff (teachers) from accessing admin unless they're superusers
        if self.is_staff and not self.is_superuser:
            return False
        return super().has_module_perms(app_label)

    def has_perm(self, perm, obj=None):
        if self.is_staff and not self.is_superuser:
            return False
        return super().has_perm(perm, obj)

    def __str__(self):
        return self.email

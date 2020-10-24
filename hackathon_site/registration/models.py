from django.db import models
from django.core import validators
from django.contrib.auth import get_user_model
import uuid

from registration.validators import UploadedFileValidator

User = get_user_model()


def _generate_team_code():
    team_code = uuid.uuid4().hex[:5].upper()
    while Team.objects.filter(team_code=team_code).exists():
        team_code = uuid.uuid4().hex[:5].upper()
    return team_code


class Team(models.Model):
    team_code = models.CharField(max_length=5, default=_generate_team_code, null=False)

    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    MAX_MEMBERS = 4

    def __str__(self):
        return self.team_code


class Application(models.Model):
    GENDER_CHOICES = [
        (None, ""),
        ("male", "Male"),
        ("female", "Female"),
        ("non-binary", "Non-binary"),
        ("other", "Other"),
        ("no-answer", "Prefer not to answer"),
    ]

    ETHNICITY_CHOICES = [
        (None, ""),
        ("american-native", "American Indian or Alaskan Native"),
        ("asian-pacific-islander", "Asian / Pacific Islander"),
        ("black-african-american", "Black or African American"),
        ("hispanic", "Hispanic"),
        ("caucasian", "White / Caucasian"),
        ("other", "Multiple ethnicity / Other"),
        ("no-answer", "Prefer not to answer"),
    ]

    STUDY_LEVEL_CHOICES = [
        (None, ""),
        ("highschool", "High School"),
        ("undergraduate", "Undergraduate"),
        ("gradschool", "Graduate School"),
        ("other", "Other"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    team = models.ForeignKey(
        Team, related_name="applications", on_delete=models.CASCADE, null=False
    )

    # User Submitted Fields
    birthday = models.DateField(null=False)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, null=False)
    ethnicity = models.CharField(max_length=50, choices=ETHNICITY_CHOICES, null=False)
    phone_number = models.CharField(
        max_length=20,
        null=False,
        validators=[
            validators.RegexValidator(
                r"^(?:\+\d{1,3})?\s?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{4}$",
                message="Enter a valid phone number.",
            )
        ],
    )
    school = models.CharField(max_length=255, null=False)
    study_level = models.CharField(
        max_length=50, choices=STUDY_LEVEL_CHOICES, null=False
    )
    graduation_year = models.IntegerField(
        null=False,
        validators=[
            validators.MinValueValidator(
                2000, message="Enter a realistic graduation year."
            ),
            validators.MaxValueValidator(
                2030, message="Enter a realistic graduation year."
            ),
        ],
    )
    program = models.CharField(max_length=255, help_text="Program or Major", null=False)
    resume = models.FileField(
        upload_to="applications/resumes/",
        validators=[
            UploadedFileValidator(
                content_types=["application/pdf"], max_upload_size=20 * 1024 * 1024
            )
        ],
        null=False,
    )
    address_line_1 = models.CharField(
        max_length=255, help_text="Address Line 1", null=True, blank=True
    )
    address_line_2 = models.CharField(
        max_length=255, help_text="Address Line 2", null=True, blank=True
    )
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(
        max_length=255, help_text="Province / State", null=True, blank=True
    )
    country = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(
        max_length=10, help_text="Postal Code", null=True, blank=True
    )

    q1 = models.TextField(
        null=False,
        help_text="Why do you want to participate in NewHacks?",
        max_length=1000,
    )
    q2 = models.TextField(
        null=False,
        help_text="Tell us about your experience with software or other topics relevant to NewHacks!",
        max_length=1000,
    )
    q3 = models.TextField(
        null=False, help_text="How did you hear about NewHacks?", max_length=100
    )
    conduct_agree = models.BooleanField(
        help_text="I have read and agree to the "
        '<a href="https://docs.google.com/document/d/1Uec_PDknY-9nSMc7QOqSTFb54I71uGX6oZaoTm1u8Q0/">code of conduct</a>.',
        blank=False,
        null=False,
    )
    data_agree = models.BooleanField(
        help_text="I consent to have the data in this application collected for event purposes "
        "including administration, ranking, and event communication, and to be shared with event "
        "sponsors and partners.",
        blank=False,
        null=False,
    )

    rsvp = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
